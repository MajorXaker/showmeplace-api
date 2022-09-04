from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields

from models.db_models import User
from ..gql_types.user import UserType


class MutationAddUser(SQLAlchemyCreateMutation):
    class Meta:
        model = User
        output = UserType
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

    # @classmethod
    # async def mutate(cls, root, info, value: dict):
    #
    #     result = await super().mutate(root, info, value)
    #
    #
    #     return result
