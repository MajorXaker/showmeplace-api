import datetime

import graphene
from alchql import SQLAlchemyCreateMutation
import sqlalchemy as sa
from utils.config import settings as s
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from graphene import ObjectType
from sqlalchemy.ext.asyncio import AsyncSession

from models.base_engine import Model
from models.db_models import (
    Place,
    SecretPlaceExtra,
    M2MUserPlaceMarked,
    Category,
    ActionsEconomy,
)
from utils.api_auth import AuthChecker
from ..gql_id import decode_gql_id
from ..gql_types.place_type import PlaceType
from ..service_types.coin_change_object import CoinChange


class PlaceAddition(ObjectType):
    added_place = graphene.Field(type_=PlaceType)
    coin_change = graphene.Field(type_=CoinChange)


class PlaceDataInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    category_id = graphene.String(required=True)
    coordinate_longitude = graphene.Float(required=True)
    coordinate_latitude = graphene.Float(required=True)

    address = graphene.String()
    description = graphene.String()


class SecretPlaceExtraInput(graphene.InputObjectType):
    food_suggestion = graphene.String()
    time_suggestion = graphene.String()
    company_suggestion = graphene.String()
    music_suggestion = graphene.String()
    extra_suggestion = graphene.String()


#
#
# class MutationAddPlace(graphene.Mutation):
#     class Arguments:
#         place_data = PlaceDataInput()
#         secret_place_extra = SecretPlaceExtraInput()
#
#     # new_place = PlaceType()
#     coin_change = CoinChange()
#
#     @staticmethod
#     def mutate(args, info, new_place):
#         coins = {
#             "change_amount": f"+100",
#             "coins": 150,
#         }
#         return MutationAddPlace(coin_change=coins)


# class MutationAddPlace(SQLAlchemyCreateMutation):
class MutationAddPlace(graphene.Mutation):
    class Arguments:
        place_data = PlaceDataInput()
        secret_place_extra = SecretPlaceExtraInput()

    # class Meta:
    #     model = Place
    #     # output = PlaceType
    #     input_fields = get_input_fields(
    #         model=Place,
    #         only_fields=[
    #             Place.name.key,
    #             Place.category_id.key,
    #             Place.description.key,
    #             Place.coordinate_longitude.key,
    #             Place.coordinate_latitude.key,
    #             Place.address.key,
    #             Place.is_secret_place.key,
    #         ],
    #         required_fields=[
    #             Place.name.key,
    #             Place.category_id.key,
    #             Place.coordinate_longitude.key,
    #             Place.coordinate_latitude.key,
    #         ],
    #     ) | get_input_fields(
    #         model=SecretPlaceExtra,
    #         only_fields=[
    #             SecretPlaceExtra.food_suggestion.key,
    #             SecretPlaceExtra.time_suggestion.key,
    #             SecretPlaceExtra.company_suggestion.key,
    #             SecretPlaceExtra.music_suggestion.key,
    #             SecretPlaceExtra.extra_suggestion.key,
    #         ],
    #     )

    coin_change = graphene.Field(type_=CoinChange)
    new_place = graphene.Field(type_=PlaceType)

    @classmethod
    async def mutate(
        cls, root, info, place_data: dict, secret_place_extra: dict | None = None
    ):
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        possible_actions = await ActionsEconomy.verify_possibility(
            session=session, user_id=user_id
        )
        new_place = await basic_mapper(Place, place_data)
        new_place[Place.owner_id] = user_id
        place_category = (
            await session.execute(
                sa.select(Category.id, Category.name).where(
                    Category.id == new_place[Place.category_id]
                )
            )
        ).fetchone()
        is_secret_place = place_category.name == s.SECRET_PLACE_NAME

        existing_places = (
            await session.execute(
                sa.select(Place.id).where(
                    sa.and_(
                        Place.owner_id == user_id,
                        Place.category_id == place_category.id,
                    )
                )
            )
        ).fetchall()
        if existing_places:
            action_name = (
                "Create new secret place"
                if is_secret_place
                else "Create a new place of the same category"
            )
        else:
            action_name = (
                "Create first secret place" if is_secret_place else "Create a place"
            )

        if not possible_actions[action_name]:
            raise ValueError(f"Insufficient coins")

        # adding a place to db
        uploaded_place_id = (
            (
                await session.execute(
                    sa.insert(Place).values(new_place).returning(Place.id)
                )
            )
            .fetchone()
            .id
        )

        if is_secret_place and secret_place_extra:
            new_secret_place_data = await basic_mapper(
                SecretPlaceExtra, secret_place_extra
            )
            # TODO SECRET PLACE EXTRA id to place
            new_secret_place_data[SecretPlaceExtra.place_id] = uploaded_place_id
            await session.execute(
                sa.insert(SecretPlaceExtra).values(new_secret_place_data)
            )
        # setting for all other places of the same type on fire
        time_to_burnout = datetime.datetime.now() + datetime.timedelta(
            hours=s.PLACE_BURNOUT_DURATION_HOURS
        )

        # set some places on fire
        await session.execute(
            sa.update(Place)
            .where(
                sa.and_(
                    Place.id != uploaded_place_id,
                    Place.category_id == place_category.id,
                    Place.active_due_date.is_(None),
                )
            )
            .values({Place.active_due_date: time_to_burnout})
            .returning(Place.id)
        )

        coin_change = await ActionsEconomy.execute(
            session=session, action_name=action_name, coin_receiver_user_id=user_id
        )
        return MutationAddPlace(
            coin_change=coin_change,
            new_place=PlaceType.get_node(info, uploaded_place_id),
        )


async def basic_mapper(classtype, value):
    new_value = {}
    for attr, attr_val in value.items():
        if "id" in attr:
            attr_val = decode_gql_id(attr_val)[1]
        if hasattr(classtype, attr):
            new_value[getattr(classtype, attr)] = attr_val
    return new_value
