from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields

from gql.gql_types.user_type import UserType
from models.db_models.m2m.m2m_user_user_following import M2MUserFollowingUser



class HasRegistration(SQLAlchemyCreateMutation):
    class Meta:
        model = M2MUserFollowingUser
        output = UserType
        input_fields = get_input_fields(
            model=M2MUserFollowingUser,
            only_fields=[
                M2MUserFollowingUser.lead_id.key,
                M2MUserFollowingUser.follower_id.key,
            ],
            required_fields=[
                M2MUserFollowingUser.lead_id.key,
                M2MUserFollowingUser.follower_id.key,
            ],
        )
