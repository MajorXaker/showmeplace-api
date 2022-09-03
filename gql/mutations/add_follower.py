# TODO

from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields

from models.db_models import User
from models.db_models.m2m_user_user_following import M2MUserFollowingUser
from ..gql_types.select_users import SelectUsers


class MutationAddFollower(SQLAlchemyCreateMutation):
    class Meta:
        model = M2MUserFollowingUser
        output = SelectUsers
        input_fields = get_input_fields(
            model=User,
            only_fields=[
                User.name.key,
                User.has_onboarded,
                User.level,
                User.coins,
            ],
            required_fields=[User.name.key],
        )
