import boto3
import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyCreateMutation
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import encode_gql_id
from models.db_models import User, EmailAddress
from models.enums import EmailStatusEnum
from utils.config import settings as s


class MutationRegistrationLoginCognito(SQLAlchemyCreateMutation):
    class Meta:
        model = User
        input_fields = {
            "user_name": graphene.String(required=True),
            "email_address": graphene.String(),
            "password": graphene.String(required=True),
        }

    registered_now = graphene.Boolean()
    registered_earlier = graphene.Boolean()
    token = graphene.String()

    @classmethod
    async def mutate(cls, root, info, value: dict):
        session: AsyncSession = info.context.session
        pool = s.COGNITO_USER_POOL
        cognito_connection = boto3.client(
            "cognito-idp",
            region_name="us-east-1",
            aws_access_key_id=s.ACCESS_KEY_ID,
            aws_secret_access_key=s.ACCESS_SECRET_KEY,
        )
        username = value["user_name"]
        raw_user_data = cognito_connection.list_users(
            UserPoolId=pool,
            Limit=1,
            Filter=f'username = "{username}"',
        )["Users"]

        if raw_user_data:
            # TODO Do we need userdata?
            response = await cls.cognito_login(
                cognito_connection=cognito_connection,
                session=session,
                username=username,
                password=value["password"],
            )
        else:
            if not value.get("email_address"):
                raise ValueError("Email is required for registration")
            response = await cls.cognito_register(
                cognito_connection=cognito_connection,
                session=session,
                username=username,
                password=value["password"],
                email=value["email_address"],
            )

        return MutationRegistrationLoginCognito(**response)

    @classmethod
    async def cognito_login(
        cls, cognito_connection, session: AsyncSession, username: str, password: str
    ):
        try:
            response = cognito_connection.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": username, "PASSWORD": password},
                ClientId=s.COGNITO_CLIENT_ID,
            )
        except cognito_connection.exceptions.NotAuthorizedException:
            raise ValueError("Incorrect username or password")

        if response["AuthenticationResult"].get("AccessToken"):
            user = (
                await session.execute(sa.select(User.id).where(User.name == username))
            ).fetchone()
            token = encode_gql_id("UserType", user.id)

            return {
                "token": token,
                "registered_earlier": True,
                "registered_now": False,
            }

    @classmethod
    async def cognito_register(
        cls,
        cognito_connection,
        session: AsyncSession,
        username: str,
        password: str,
        email: str,
    ):
        if "@" not in email:
            raise ValueError("Email address incorrect")
        sign_up_response = cognito_connection.sign_up(
            ClientId=s.COGNITO_CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
            ],
        )
        # TODO Routine for confirming email!!!!
        confirm_sign_up_response = cognito_connection.admin_confirm_sign_up(
            UserPoolId=s.COGNITO_USER_POOL, Username=username
        )
        email_status = EmailStatusEnum.VERIFIED
        # TODO Routine for confirming email!!!!

        new_user_id = (
            await session.execute(
                sa.insert(User)
                .values(
                    {
                        User.name: username,
                        User.external_id: username,
                        User.external_id_type: "COGNITO",
                        User.coins: 0,
                        User.level: 0,
                    }
                )
                .returning(User.id)
            )
        ).fetchone()

        # internal_id = encode_gql_id("UserType", new_user_id.id)

        await session.execute(
            sa.insert(EmailAddress).values(
                {
                    EmailAddress.address: email,
                    EmailAddress.user_id: new_user_id.id,
                    EmailAddress.status: email_status,
                }
            )
        )

        internal_id = (
            await cls.cognito_login(
                cognito_connection=cognito_connection,
                session=session,
                username=username,
                password=password,
            )
        )["token"]

        return {
            "token": internal_id,
            "registered_earlier": False,
            "registered_now": True,
        }
