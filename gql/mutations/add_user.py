from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields

from models.db_models import User
from ..gql_types.user_type import UserType


class MutationAddUser(SQLAlchemyCreateMutation):
    class Meta:
        model = User
        output = UserType
        input_fields = get_input_fields(
            model=User,
            exclude_fields=[
                User.level.key,
                User.coins.key,
            ],
            required_fields=[
                User.name.key,
                User.cognito_user_id.key,
            ],
        )

    # @classmethod
    # async def mutate(cls, root, info, value: dict):
    #
    #     result = await super().mutate(root, info, value)
    #
    #
    #     return result
