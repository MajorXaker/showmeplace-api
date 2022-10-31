import datetime

import graphene
import sqlalchemy as sa
from graphene import ObjectType
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models import (
    Place,
    SecretPlaceExtra,
    Category,
    ActionsEconomy,
)
from utils.api_auth import AuthChecker
from utils.config import settings as s
from utils.smp_exceptions import Exc, ExceptionGroupEnum, ExceptionReasonEnum
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


class MutationAddPlace(graphene.Mutation):
    class Arguments:
        place_data = PlaceDataInput()
        secret_place_extra = SecretPlaceExtraInput()

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

        if not is_secret_place and secret_place_extra is not None:
            Exc.value(
                message="It is not possible to enter the data of a secret place in a normal place",
                of_group=ExceptionGroupEnum.BAD_INPUT,
                reasons=ExceptionReasonEnum.INCORRECT_VALUE,
            )

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
            Exc.low_wallet(
                message="Insufficient coins",
                of_group=ExceptionGroupEnum.BAD_BALANCE,
                reasons=ExceptionReasonEnum.LOW_BALANCE,
            )

        # adding a place to db
        if is_secret_place and secret_place_extra:
            new_secret_place_data = await basic_mapper(
                SecretPlaceExtra, secret_place_extra
            )
            secret_place_id = (
                await session.execute(
                    sa.insert(SecretPlaceExtra)
                    .values(new_secret_place_data)
                    .returning(SecretPlaceExtra.id)
                )
            ).scalar()
        else:
            secret_place_id = None
        new_place[Place.secret_extra_id] = secret_place_id
        uploaded_place_id = (
            (
                await session.execute(
                    sa.insert(Place).values(new_place).returning(Place.id)
                )
            )
            .fetchone()
            .id
        )

        # setting for all other places of the same type on fire
        time_to_decay = datetime.datetime.now() + datetime.timedelta(
            hours=s.PLACE_DECAY_DURATION_HOURS
        )
        # set some places on fire
        await session.execute(
            sa.update(Place)
            .where(
                sa.and_(
                    Place.owner_id == user_id,
                    Place.id != uploaded_place_id,
                    Place.category_id == place_category.id,
                    Place.active_due_date.is_(None),
                )
            )
            .values({Place.active_due_date: time_to_decay})
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
    # TODO Document this piece of code - Ougen*
    # TODO remove async pollution here - Ougen*
    new_value = {}
    for attr, attr_val in value.items():
        if "id" in attr:
            attr_val = decode_gql_id(attr_val)[1]
        if hasattr(classtype, attr):
            new_value[getattr(classtype, attr)] = attr_val
    return new_value
