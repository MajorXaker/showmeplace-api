import boto3
import graphene
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models import User, EmailAddress
from utils.config import settings as s
from utils.smp_exceptions import Exc, ExceptionGroupEnum, ExceptionReasonEnum


class MutationForgotPassword(graphene.Mutation):
    class Meta:
        arguments = {"user_name": graphene.String(required=True)}

    is_success = graphene.Boolean()

    @classmethod
    async def mutate(cls, root, info, user_name: dict):
        session: AsyncSession = info.context.session

        user = (
            await session.execute(
                sa.select(User.name, EmailAddress.address)
                .join(EmailAddress, EmailAddress.id == User.active_email_address_id)
                .where(User.name == user_name)
            )
        ).fetchone()

        cognito_connection = boto3.client(
            "cognito-idp",
            region_name="us-east-1",
            aws_access_key_id=s.ACCESS_KEY_ID,
            aws_secret_access_key=s.ACCESS_SECRET_KEY,
        )

        try:
            response = cognito_connection.admin_reset_user_password(
                UserPoolId=s.COGNITO_USER_POOL, Username=user_name
            )
        except cognito_connection.exceptions.UserNotFoundException:
            Exc.value(
                message=f"User '{user_name}' does not exits",
                of_group=ExceptionGroupEnum.BAD_CREDENTIALS,
                reasons=ExceptionReasonEnum.INCORRECT_VALUE,
            )

        return MutationForgotPassword(is_success=True)
