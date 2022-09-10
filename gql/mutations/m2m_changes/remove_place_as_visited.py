from alchql import SQLAlchemyDeleteMutation
from alchql.get_input_type import get_input_fields

from gql.gql_types.place_type import PlaceType
from models.db_models import User, Place
from models.db_models.m2m.m2m_user_place_visited import M2MUserPlaceVisited


class MutationAddFavouritePlace(SQLAlchemyDeleteMutation):
    class Meta:
        model = M2MUserPlaceVisited
        output = PlaceType
        input_fields = get_input_fields(
            model=User,
            only_fields=[User.id.key],
            required_fields=[User.id.key],
        ) | get_input_fields(
            model=Place,
            only_fields=[Place.id.key],
            required_fields=[Place.id.key],
        )

    # @classmethod
    # async def mutate(cls, root, info, value: dict):
    #
    #     result = await super().mutate(root, info, value)
    #
    #
    #     return result
