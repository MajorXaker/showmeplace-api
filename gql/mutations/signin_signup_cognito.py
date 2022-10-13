import re

import boto3
import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyCreateMutation
from graphql import GraphQLResolveInfo
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import encode_gql_id
from models.db_models import User, EmailAddress
from models.enums import EmailStatusEnum
from utils.config import settings as s
from utils.smp_exceptions import Exc, ExceptionGroupEnum, ExceptionReasonEnum


class PasswordReset(graphene.InputObjectType):
    confirmation_code = graphene.String(required=True)
    new_password = graphene.String(required=True)


class MutationSigninSignupCognito(SQLAlchemyCreateMutation):
    class Meta:
        model = User
        arguments = {
            "user_name": graphene.String(required=True),
            "email_address": graphene.String(),
            "password": graphene.String(required=True),
            "password_reset_box": PasswordReset(),
            "is_registration": graphene.Boolean(),
        }
        name = "MutationSignInSignUp"

    registered_now = graphene.Boolean()
    registered_earlier = graphene.Boolean()
    token = graphene.String()

    @classmethod
    async def mutate(cls, root, info, **value: dict):
        session: AsyncSession = info.context.session
        cognito_connection = boto3.client(
            "cognito-idp",
            region_name="us-east-1",
            aws_access_key_id=s.ACCESS_KEY_ID,
            aws_secret_access_key=s.ACCESS_SECRET_KEY,
        )
        username: str = value["user_name"].strip()
        if len(username) < 2:
            Exc.value(
                message="Username is too short",
                of_group=ExceptionGroupEnum.BAD_CREDENTIALS,
                reasons=ExceptionReasonEnum.LONGER_2,
            )
        raw_user_data = cognito_connection.list_users(
            UserPoolId=s.COGNITO_USER_POOL,
            Limit=1,
            Filter=f'username = "{username}"',
            # )[0]
        )["Users"]
        is_registration = value.get("is_registration")

        if is_registration and not raw_user_data:
            if not value.get("email_address"):
                Exc.value(
                    message="Email is required for registration.",
                    of_group=ExceptionGroupEnum.EMAIL,
                    reasons=ExceptionReasonEnum.MISSING_VALUE,
                )
            response = await cls.cognito_register(
                cognito_connection=cognito_connection,
                session=session,
                username=username,
                password=value["password"],
                email=value["email_address"],
            )

        if not is_registration and raw_user_data:
            if raw_user_data[0]["UserStatus"] == "RESET_REQUIRED":
                if "password_reset_box" not in value:
                    Exc.value(
                        message="No password reset data",
                        of_group=ExceptionGroupEnum.PASSWORD_RESET,
                        reasons=ExceptionReasonEnum.MISSING_VALUE,
                    )
                await cls.reset_password(
                    cognito_connection=cognito_connection,
                    info=info,
                    username=username,
                    password_reset_box=value["password_reset_box"],
                )
            # TODO Do we need userdata?
            response = await cls.cognito_login(
                cognito_connection=cognito_connection,
                session=session,
                username=username,
                password=value["password"],
            )
        if not is_registration and not raw_user_data:
            Exc.value(
                message="User is not registered",
                of_group=ExceptionGroupEnum.BAD_CREDENTIALS,
                reasons=ExceptionReasonEnum.INCORRECT_VALUE,
            )
        if is_registration and raw_user_data:
            Exc.value(
                message="Username already in use",
                of_group=ExceptionGroupEnum.BAD_CREDENTIALS,
                reasons=(
                    ExceptionReasonEnum.INCORRECT_VALUE,
                    ExceptionReasonEnum.VALUE_IN_USE,
                ),
            )

        return MutationSigninSignupCognito(**response)

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
            Exc.value(
                message="Incorrect username or password",
                of_group=ExceptionGroupEnum.BAD_CREDENTIALS,
                reasons=ExceptionReasonEnum.INCORRECT_VALUE,
            )
            return
        except cognito_connection.exceptions.UserNotConfirmedException:
            Exc.value(
                message="Email address is not confirmed",
                of_group=ExceptionGroupEnum.EMAIL,
                reasons=ExceptionReasonEnum.NOT_CONFIRMED,
            )
            return
        except cognito_connection.exceptions.PasswordResetRequiredException:
            Exc.value(
                message="User has requested a password change",
                of_group=ExceptionGroupEnum.BAD_CREDENTIALS,
                reasons=ExceptionReasonEnum.CHANGE_REQUESTED,
            )
            return
        if response["AuthenticationResult"].get("AccessToken"):
            user = (
                await session.execute(
                    sa.select(
                        User.id,
                        User.name,
                        User.active_email_address_id,
                        EmailAddress.status.label("email_status"),
                    )
                    .join(EmailAddress, EmailAddress.id == User.active_email_address_id)
                    .where(User.name == username)
                )
            ).fetchone()
            if user.email_status != EmailStatusEnum.VERIFIED:
                if user.email_status == EmailStatusEnum.PENDING:
                    await session.execute(
                        sa.update(EmailAddress)
                        .where(EmailAddress.id == user.active_email_address_id)
                        .values({EmailAddress.status: EmailStatusEnum.VERIFIED})
                    )
                else:
                    # todo wunno what could happen to trigger this. Need to think of it
                    Exc.value(
                        message="Incorrect email address. Contact ShowMePlace team",
                        of_group=ExceptionGroupEnum.EMAIL,
                        reasons=ExceptionReasonEnum.INCORRECT_VALUE,
                    )

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
        # TODO remove user if hasn't verified email in 24 hours and tried to use same credentials again
        q = sa.select(EmailAddress.id).where(
            EmailAddress.address == email,

        )
        email_in_use = (await session.execute(q)).fetchone()
        if email_in_use:
            Exc.value(
                message="Email address already in use",
                of_group=ExceptionGroupEnum.EMAIL,
                reasons=(
                    ExceptionReasonEnum.DUPLICATE_VALUE,
                    ExceptionReasonEnum.VALUE_IN_USE,
                ),
            )

        if "@" not in email:
            Exc.value(
                message="Email address incorrect",
                of_group=ExceptionGroupEnum.EMAIL,
                reasons=ExceptionReasonEnum.INCORRECT_VALUE,
            )

        if len(password) < 6:
            pass

        password_errors = {}
        if len(password) < 6:
            password_errors[
                "Password should be at least 6 symbols"
            ] = ExceptionReasonEnum.LONGER_6
        if not re.findall(r"\d", password):
            password_errors[
                "Password should contain at least 1 number"
            ] = ExceptionReasonEnum.NUMBER_MUST_PRESENT

        if password_errors:
            Exc.value(
                message=". ".join(password_errors.keys()),
                of_group=ExceptionGroupEnum.PASSWORD,
                reasons=list(password_errors.values()),
            )

        # # TODO Routine for confirming email!!!!
        # confirm_sign_up_response = cognito_connection.admin_confirm_sign_up(
        #     UserPoolId=s.COGNITO_USER_POOL, Username=username
        # )
        email_status = EmailStatusEnum.PENDING
        try:
            sign_up_response = cognito_connection.sign_up(
                ClientId=s.COGNITO_CLIENT_ID,
                Username=username,
                Password=password,
                UserAttributes=[
                    {"Name": "email", "Value": email},
                    # {"Name": "custom:creator", "Value": s.MACHINE_NAME},
                ],
            )
        except cognito_connection.exceptions.InvalidPasswordException:
            Exc.value(
                message="Password invalid",
                of_group=ExceptionGroupEnum.PASSWORD,
                reasons=ExceptionReasonEnum.INCORRECT_VALUE,
            )
        except cognito_connection.exceptions.UsernameExistsException:
            Exc.value(
                message="Username already taken",
                of_group=ExceptionGroupEnum.BAD_CREDENTIALS,
                reasons=ExceptionReasonEnum.INCORRECT_VALUE,
            )

        email_row = (
            await session.execute(
                sa.insert(EmailAddress)
                .values(
                    {
                        EmailAddress.address: email,
                        EmailAddress.status: email_status,
                    }
                )
                .returning(EmailAddress.id)
            )
        ).fetchone()

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
                        User.active_email_address_id: email_row.id,
                    }
                )
                .returning(User.id)
            )
        ).fetchone()

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

    @classmethod
    async def reset_password(
        cls,
        cognito_connection,
        info: GraphQLResolveInfo,
        username: str,
        password_reset_box: dict,
    ):
        if not all(
            [
                "new_password" in password_reset_box,
                "confirmation_code" in password_reset_box,
            ]
        ):
            Exc.value(
                message="No password reset data incomplete",
                of_group=ExceptionGroupEnum.PASSWORD_RESET,
                reasons=ExceptionReasonEnum.MISSING_VALUE,
            )
        # TODO EXTREME VULNURABILITY! NO CODE IS NECESSARY ATM!!!
        response = cognito_connection.admin_set_user_password(
            UserPoolId=s.COGNITO_USER_POOL,
            Username=username,
            Password=password_reset_box["new_password"],
            Permanent=True,
        )

        # response = cognito_connection.admin_respond_to_auth_challenge(
        #     UserPoolId=s.COGNITO_USER_POOL,
        #     ClientId=s.COGNITO_CLIENT_ID,
        #     ChallengeName='NEW_PASSWORD_REQUIRED',
        #     ChallengeResponses={
        #         'PASSWORD': password_reset_box["new_password"]
        #         'PASSWORD': password_reset_box["new_password"]
        #     },
        #     Session='string',
        #     AnalyticsMetadata={
        #         'AnalyticsEndpointId': 'string'
        #     },
        #     ContextData={
        #         'IpAddress': 'string',
        #         'ServerName': 'string',
        #         'ServerPath': 'string',
        #         'HttpHeaders': [
        #             {
        #                 'headerName': 'string',
        #                 'headerValue': 'string'
        #             },
        #         ],
        #         'EncodedData': 'string'
        #     },
        #     ClientMetadata={
        #         'string': 'string'
        #     }
        # )
