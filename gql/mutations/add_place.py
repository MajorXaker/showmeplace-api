import graphene
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from models.db_models import User, Place, SecretPlaceExtra, M2MUserPlaceMarked
from ..gql_id import decode_gql_id
from ..gql_types.place_type import PlaceType
from ..gql_types.user_type import UserType


class MutationAddPlace(SQLAlchemyCreateMutation):
    class Meta:
        model = Place
        output = PlaceType
        input_fields = (
            get_input_fields(
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
            )
            | get_input_fields(
                model=SecretPlaceExtra,
                only_fields=[
                    SecretPlaceExtra.food_suggestion.key,
                    SecretPlaceExtra.time_suggestion.key,
                    SecretPlaceExtra.company_suggestion.key,
                    SecretPlaceExtra.music_suggestion.key,
                    SecretPlaceExtra.extra_suggestion.key,
                ],
            )
            | {"user__id": graphene.ID(required=True)}
        )
        # get_input_fields(
        #     model=User,
        #     only_fields=[User.id.key],
        #     required_fields=[User.id.key]
        #
        # )

    @classmethod
    async def mutate(cls, root, info, value: dict):
        session: AsyncSession = info.context.session
        user_id = decode_gql_id(value.pop("user__id"))[1]
        result = await super().mutate(root, info, value)
        await session.execute(
            sa.insert(M2MUserPlaceMarked).values(
                {
                    M2MUserPlaceMarked.place_id: result.id,
                    M2MUserPlaceMarked.user_id: user_id,
                }
            )
        )
        return result
