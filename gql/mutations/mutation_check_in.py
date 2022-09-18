import math

import graphene
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from utils.config import settings as s
from models.db_models import Place
from models.db_models.m2m.m2m_user_place_visited import M2MUserPlaceVisited
from ..gql_id import decode_gql_id


class MutationCheckIn(graphene.Mutation):
    class Arguments:
        user__checking_in__id = graphene.String(required=True)
        check_in__place__id = graphene.String(required=True)
        user__latitude = graphene.Float(required=True)
        user__longitude = graphene.Float(required=True)

    is_success = graphene.Boolean()

    @classmethod
    async def mutate(
        cls,
        root,
        info,
        user__checking_in__id: str,
        check_in__place__id: str,
        user__latitude: float,
        user__longitude: float,
    ):
        session: AsyncSession = info.context.session

        lat = info.variable_values["userLatitude"]
        long = info.variable_values["userLongitude"]
        dist = 1000 / s.CHECK_IN_DISTANCE

        delta_latitude = dist / 111  # 1 lat degree is roughly 111 km
        longitude_1_degree_length = 111.3 * math.cos(lat)
        delta_longitude = dist / longitude_1_degree_length

        place_id = decode_gql_id(check_in__place__id)[1]
        user_id = decode_gql_id(user__checking_in__id)[1]
        is_been_here = await session.execute(
            sa.select(M2MUserPlaceVisited.user_id).where(
                sa.and_(
                    M2MUserPlaceVisited.user_id == user_id,
                    M2MUserPlaceVisited.place_id == place_id,
                )
            )
        )
        if is_been_here:
            raise ValueError("User has already been here")
        # TODO go to try-except logic
        place = (
            await session.execute(
                sa.select(Place.id).where(
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
            return MutationCheckIn(is_success=True)
        else:
            return MutationCheckIn(is_success=False)
