import graphene
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import decode_gql_id
from models.db_models.m2m.m2m_user_user_following import M2MUserFollowingUser
from utils.api_auth import AuthChecker


class MutationRemoveFollower(graphene.Mutation):
    class Meta:
        model = M2MUserFollowingUser
        arguments = {
            "lead_id": graphene.String(required=True),
        }

    is_success = graphene.Boolean()

    @classmethod
    async def mutate(cls, root, info, lead_id: str):
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        lead_id = decode_gql_id(lead_id)[1]
        if user_id == lead_id:
            raise ValueError("You can't unfollow yourself")

        await session.execute(
            sa.delete(M2MUserFollowingUser).where(
                sa.and_(
                    M2MUserFollowingUser.follower_id == user_id,
                    M2MUserFollowingUser.lead_id == lead_id,
                )
            )
        )

        return MutationRemoveFollower(is_success=True)
