from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import decode_gql_id
from gql.gql_types.user_type import UserType
from models.db_models.m2m.m2m_user_user_following import M2MUserFollowingUser
from utils.api_auth import AuthChecker


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

    @classmethod
    async def mutate(cls, root, info, value: dict):
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        lead_id = decode_gql_id(value["lead_id"])[1]
        if user_id == lead_id:
            raise ValueError("You can't follow yourself")
        value["follower_id"] = user_id
        value["lead_id"] = lead_id
        result = await super().mutate(root, info, value)

        return result
