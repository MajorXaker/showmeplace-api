import datetime
import logging
import math

import graphene
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from utils.api_auth import AuthChecker
from utils.config import settings as s
from models.db_models import Place, ActionsEconomy, Category
from models.db_models.m2m.m2m_user_place_visited import M2MUserPlaceVisited
from ..gql_id import decode_gql_id
from ..service_types.coin_change_object import CoinChange


class MutationCheckIn(graphene.Mutation):
    class Arguments:
        check_in__place__id = graphene.String(required=True)
        user__latitude = graphene.Float(required=True)
        user__longitude = graphene.Float(required=True)

    is_success = graphene.Boolean()
    coin_change = graphene.Field(type_=CoinChange)

    @classmethod
    async def mutate(
        cls,
        root,
        info,
        check_in__place__id: str,
        user__latitude: float,
        user__longitude: float,
    ):
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        lat = info.variable_values["userLatitude"]
        long = info.variable_values["userLongitude"]
        dist = s.CHECK_IN_DISTANCE / 1000
        place_id = decode_gql_id(check_in__place__id)[1]

        logging.debug(
            f"EVENT: {datetime.datetime.now()}."
            f"User ID#{user_id}, checks in place ID#{place_id}. "
            f"Dist={dist} km. User coords: Lat={lat}, Long={long}."
        )
        # logging.debug(f"Current check-in distance is: {dist}")
        delta_latitude = abs(dist / 111)  # 1 lat degree is roughly 111 km
        longitude_1_degree_length = 111.3 * math.cos(lat)
        delta_longitude = abs(dist / longitude_1_degree_length)

        is_been_here = (
            await session.execute(
                sa.select(M2MUserPlaceVisited.user_id).where(
                    sa.and_(
                        M2MUserPlaceVisited.user_id == user_id,
                        M2MUserPlaceVisited.place_id == place_id,
                    )
                )
            )
        ).fetchone()
        if is_been_here:
            raise ValueError("User has already been here")
        # TODO go to try-except logic
        place = (
            await session.execute(
                sa.select(
                    Place.id, Place.owner_id, Category.name.label("category_name")
                )
                .join(Category, Place.category_id == Category.id)
                .where(
                    sa.and_(
                        Place.id == place_id,
                        sa.func.ABS(Place.coordinate_longitude - long)
                        < delta_longitude,
                        sa.func.ABS(Place.coordinate_latitude - lat) < delta_latitude,
                    )
                )
            )
        ).fetchone()
        if place:
            await session.execute(
                sa.insert(M2MUserPlaceVisited).values(
                    [
                        {
                            M2MUserPlaceVisited.user_id: user_id,
                            M2MUserPlaceVisited.place_id: place_id,
                        }
                    ]
                )
            )
            visited_place_action = (
                "Have your secret place visited"
                if place.category_name == s.SECRET_PLACE_NAME
                else "Have your place visited"
            )
            # toss a coin to place owner
            await ActionsEconomy.execute(
                session=session,
                action_name=visited_place_action,
                coin_receiver_user_id=place.owner_id,
            )
            coin_change_actor = await ActionsEconomy.execute(
                session=session,
                action_name="Visit a place",
                coin_receiver_user_id=user_id,
            )
            return MutationCheckIn(is_success=True, coin_change=coin_change_actor)
        else:
            return MutationCheckIn(is_success=False, coin_change=None)
