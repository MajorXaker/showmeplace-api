from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields

from models.db_models import User, Place
from ..gql_types.select_places import SelectPlaces
from ..gql_types.select_users import SelectUsers


class MutationAddPlace(SQLAlchemyCreateMutation):
    class Meta:
        model = Place
        output = SelectPlaces
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
