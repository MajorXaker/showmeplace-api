import graphene
from alchql import SQLAlchemyCreateMutation
import sqlalchemy as sa
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from graphene import ObjectType
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models import Place, SecretPlaceExtra, M2MUserPlaceMarked
from utils.api_auth import AuthChecker
from ..gql_types.place_type import PlaceType
from ..service_types.coin_change_object import CoinChange

# class PlaceAddition(ObjectType):
#     added_place = graphene.Field(type_=PlaceType)
#     coin_change = graphene.Field(type_=CoinChange)


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

    coin_change = graphene.Field(type_=CoinChange)


    @classmethod
    async def mutate(cls, root, info, value: dict, **kwargs):
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        # value["coin_change"] = {
        #     "change_amount": f"- 50",
        #     "coins": 2250,
        # }
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
