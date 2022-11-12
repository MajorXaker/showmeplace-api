import boto3
import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import encode_gql_id
from models.db_models import User, EmailAddress
from models.enums import EmailStatusEnum
from utils.config import settings as s


class MutationVerifyCognitoUser(SQLAlchemyCreateMutation):
    class Meta:
        model = User
        input_fields = {
            "user_name": graphene.String(),
            "email_address": graphene.String(required=True),
        }

    registered_now = graphene.Boolean()
    registered_earlier = graphene.Boolean()
    internal_id = graphene.String()

    @classmethod
    async def mutate(cls, root, info, value: dict):
        session: AsyncSession = info.context.session
        if False:
            # TODO section logic when email is incorrect
            raise ValueError("Incorrect email! Change email address")

        cognito_connection = boto3.client(
            "cognito-idp",
            region_name="us-east-1",
            aws_access_key_id=s.ACCESS_KEY_ID,
            aws_secret_access_key=s.ACCESS_SECRET_KEY,
        )
        # status could be 'CONFIRMED' or 'UNCONFIRMED'
        email_address = value["email_address"]
        user_data = cognito_connection.list_users(
            UserPoolId="us-east-1_60d3tsON2",
            Limit=1,
            Filter=f'email = "{email_address}"',
        )
        the_user = user_data["Users"][0]
        if the_user["UserStatus"] == "UNCONFIRMED":
            raise PermissionError("Email has not been verified yet!")
        user_attribute = dict(
            zip(
                (x["Name"] for x in the_user["Attributes"]),
                (x["Value"] for x in the_user["Attributes"]),
            )
        )
        user_in_base = (
            await session.execute(
                sa.select(User.external_id, User.id).where(
                    User.external_id == user_attribute["sub"]
                )
            )
        ).fetchone()
        if user_in_base:
            internal_id = encode_gql_id("UserType", user_in_base.id)
            return MutationVerifyCognitoUser(
                registered_earlier=True,
                registered_now=False,
                internal_id=internal_id,
            )
        if not value["user_name"]:
            value["user_name"] = value["email_address"]
        new_user_id = (
            await session.execute(
                sa.insert(User)
                .values(
                    {
                        User.name: value["user_name"],
                        User.external_id: user_attribute["sub"],
                        User.external_id_type: "COGNITO",
                        User.coins: s.STARTING_COINS,
                        User.level: 0,
                    }
                )
                .returning(User.id)
            )
        ).fetchone()
        internal_id = encode_gql_id("UserType", new_user_id.id)

        await session.execute(
            sa.insert(EmailAddress).values(
                {
                    EmailAddress.address: value["email_address"],
                    EmailAddress.user_id: new_user_id.id,
                    EmailAddress.status: EmailStatusEnum.VERIFIED,
                }
            )
        )

        return MutationVerifyCognitoUser(
            registered_earlier=False,
            registered_now=True,
            internal_id=internal_id,
        )
