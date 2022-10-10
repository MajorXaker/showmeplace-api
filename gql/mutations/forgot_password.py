import boto3
import graphene
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import decode_gql_id
from gql.gql_types.place_type import PlaceType
from models.db_models import User, EmailAddress
from models.db_models.m2m.m2m_user_place_favourite import M2MUserPlaceFavourite
from utils.api_auth import AuthChecker
import sqlalchemy as sa
from utils.config import settings as s
from utils.smp_exceptions import Exc, ExceptionGroupEnum, ExceptionReasonEnum


class MutationForgotPassword(graphene.Mutation):
    class Meta:
        # model = M2MUserOpenedSecretPlace
        # output = PlaceType
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
                UserPoolId=s.COGNITO_USER_POOL,
                Username=user_name
            )
        except cognito_connection.exceptions.UserNotFoundException:
            Exc.value(
                message=f"User '{user_name}' does not exits",
                of_group=ExceptionGroupEnum.BAD_CREDENTIALS,
                reasons=ExceptionReasonEnum.INCORRECT_VALUE,
            )

        return MutationForgotPassword(is_success=True)
