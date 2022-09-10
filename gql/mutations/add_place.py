from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields

from models.db_models import User, Place, SecretPlaceExtra
from ..gql_types.place_type import PlaceType
from ..gql_types.user_type import UserType


class MutationAddPlace(SQLAlchemyCreateMutation):
    class Meta:
        model = Place
        output = PlaceType
        input_fields = get_input_fields(
            model=Place,
            only_fields=[
                Place.name.key,
                Place.category_id.key,
                Place.description.key,
                Place.coordinate_longitude.key,
                Place.coordinate_latitude.key,
                Place.address.key,
                Place.is_secret_place.key,
            ],
            required_fields=[
                Place.name.key,
                Place.category_id.key,
                Place.coordinate_longitude.key,
                Place.coordinate_latitude.key,
            ],
        ) | get_input_fields(
            model=SecretPlaceExtra,
            only_fields=[
                SecretPlaceExtra.food_suggestion.key,
                SecretPlaceExtra.time_suggestion.key,
                SecretPlaceExtra.company_suggestion.key,
                SecretPlaceExtra.music_suggestion.key,
                SecretPlaceExtra.extra_suggestion.key,
            ],
        )

    @classmethod
    async def mutate(cls, root, info, value: dict):
        # TODO inner logic
        result = await super().mutate(root, info, value)

        return result
