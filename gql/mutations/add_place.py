from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields

from models.db_models import User, Place
from ..gql_types.place import PlaceType
from ..gql_types.user import UserType


class MutationAddPlace(SQLAlchemyCreateMutation):
    class Meta:
        model = Place
        output = PlaceType
        input_fields = get_input_fields(
            model=Place,
            only_fields=[
                Place.name.key,
                Place.category_id.key,
                Place.description,
                Place.coordinate_longitude,
                Place.coordinate_latitude,
                Place.address.key,
            ],
            required_fields=[
                Place.name.key,
                Place.category_id.key,
                Place.coordinate_longitude,
                Place.coordinate_latitude
            ],
        )
    # TODO add flag "is_secret_place" if secret place

    # @classmethod
    # async def mutate(cls, root, info, value: dict):
    #
    #     result = await super().mutate(root, info, value)
    #
    #
    #     return result
