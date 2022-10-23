import graphene
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import decode_gql_id
from gql.gql_types.user_type import UserType
from models.db_models.m2m.m2m_user_user_following import M2MUserFollowingUser
from utils.api_auth import AuthChecker
import sqlalchemy as sa

from utils.smp_exceptions import Exc, ExceptionGroupEnum, ExceptionReasonEnum


class MutationAddFollower(SQLAlchemyCreateMutation):
    class Meta:
        model = M2MUserFollowingUser
        output = UserType
        input_fields = get_input_fields(
            model=M2MUserFollowingUser,
            only_fields=[
                M2MUserFollowingUser.lead_id.key,
            ],
            required_fields=[
                M2MUserFollowingUser.lead_id.key,
            ],
        )

    is_success = graphene.Boolean()

    @classmethod
    async def mutate(cls, root, info, value: dict):
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        lead_id = decode_gql_id(value["lead_id"])[1]
        if user_id == lead_id:
            Exc.value(
                message="Insufficient coins",
                of_group=ExceptionGroupEnum.BAD_FOLLOWER,
                reasons=(
                    ExceptionReasonEnum.DUPLICATE_VALUE,
                    ExceptionReasonEnum.SELF_ACTION,
                ),
            )
        # value["follower_id"] = user_id
        # value["lead_id"] = lead_id
        # result = await super().mutate(root, info, value)
        insert = (
            sa.dialects.postgresql.insert(M2MUserFollowingUser).values(
                {
                    M2MUserFollowingUser.lead_id: lead_id,
                    M2MUserFollowingUser.follower_id: user_id,
                }
            )
        ).on_conflict_do_nothing(index_elements=["lead_id", "follower_id"])

        await session.execute(insert)

        return MutationAddFollower(is_success=True)
