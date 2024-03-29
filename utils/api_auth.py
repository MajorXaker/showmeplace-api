import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import decode_gql_id
from models.db_models import User
from utils.smp_exceptions import Exc, ExceptionGroupEnum, ExceptionReasonEnum


class AuthChecker:
    @classmethod
    def check_auth_request(cls, info):
        for header in info.context.request.headers.raw:
            if header[0] == b"authorization":
                active_user = header[1]
                user_id = decode_gql_id(active_user)[1]
                return user_id

        Exc.value(
            message="Unauthorized connection",
            of_group=ExceptionGroupEnum.BAD_TOKEN,
            reasons=ExceptionReasonEnum.MISSING_VALUE,
        )

    @classmethod
    async def check_auth_mutation(cls, session: AsyncSession, info):
        user_id = cls.check_auth_request(info)
        is_user_in_db = (
            await session.execute(sa.select(User.id).where(User.id == user_id))
        ).fetchone()
        if not is_user_in_db:
            Exc.value(
                message="Unauthorized connection",
                of_group=ExceptionGroupEnum.BAD_TOKEN,
                reasons=ExceptionReasonEnum.INCORRECT_TOKEN,
            )
        return user_id
