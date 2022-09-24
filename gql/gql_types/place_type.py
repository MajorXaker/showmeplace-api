import datetime
import math
from utils.config import settings as s
import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyObjectType, gql_types
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode
from alchql.utils import FilterItem
from graphene import ObjectType, String
from sqlalchemy.ext.asyncio import AsyncSession
from unidecode import unidecode

from gql.gql_id import decode_gql_id, encode_gql_id
from gql.gql_types.category_type import CatImage
from models.db_models import (
    Place,
    M2MUserPlaceMarked,
    M2MUserPlaceFavourite,
    PlaceImage,
    Category,
    CategoryImage,
)
from models.db_models.m2m.m2m_user_place_visited import M2MUserPlaceVisited
from utils.api_auth import AuthChecker

# from gql.utils.gql_id import encode_gql_id
from utils.pars_query import parse_query
from utils.s3_object_tools import get_presigned_url


class Cat(ObjectType):
    name = String()
    # filename = String()
    # description = String()
    category_images = graphene.List(of_type=CatImage)


# TODO BURNED OUT PLACES
class PlaceType(SQLAlchemyObjectType):
    class Meta:
        filter_fields = {
            Place.id: [OP_EQ, OP_IN],
            Place.category_id: [OP_EQ, OP_IN],
            "latitude_from": FilterItem(field_type=graphene.Float, filter_func=None),
            "longitude_from": FilterItem(field_type=graphene.Float, filter_func=None),
            "distance_from": FilterItem(field_type=graphene.Float, filter_func=None),
            "include_my_places": FilterItem(
                field_type=graphene.Boolean, filter_func=None
            ),
            "user_owner": FilterItem(field_type=graphene.String, filter_func=None),
            "user_favourite": FilterItem(field_type=graphene.String, filter_func=None),
            "user_visited": FilterItem(field_type=graphene.String, filter_func=None),
            "name_ilike": FilterItem(
                field_type=graphene.String,
                filter_func=lambda x: sa.func.to_tsvector(Place.name).op("@@")(
                    parse_query(unidecode(x))
                ),
            ),
            "show_secret_places": FilterItem(
                field_type=graphene.Boolean, filter_func=None
            ),  # hidden usually
            "show_decayed_places": FilterItem(
                field_type=graphene.Boolean, filter_func=None
            ),  # hidden usually
        }

        model = Place
        interfaces = (AsyncNode,)
        only_fields = [
            Place.id.key,
            Place.name.key,
            Place.description.key,
            Place.coordinate_longitude.key,
            Place.coordinate_latitude.key,
            # Place.owner_id.key,
            # "owner_id",
        ]

    category_data = graphene.Field(type_=Cat)
    images = graphene.List(of_type=graphene.String)
    is_decaying = graphene.Boolean()
    has_decayed = graphene.Boolean()
    owner_id = gql_types.String(model_field=Place.owner_id)



    async def resolve_category_data(self, info):
        session: AsyncSession = info.context.session
        raw_cat_id = (
            (
                await session.execute(
                    sa.select(Place.category_id).where(Place.id == self.id)
                )
            )
            .fetchone()
            .category_id
        )
        cat_id = encode_gql_id(
            "CategoryType",
            raw_cat_id,
        )
        category_name = (
            (
                await session.execute(
                    sa.select(Category.name).where(Category.id == raw_cat_id)
                )
            )
            .fetchone()
            .name
        )

        images = (
            await session.execute(
                sa.select(
                    CategoryImage.id,
                    CategoryImage.s3_filename,
                    CategoryImage.description,
                ).where(CategoryImage.category_id == raw_cat_id)
            )
        ).fetchall()
        category_images = []
        if images:
            category_images = [
                {
                    "presigned_url": await get_presigned_url(
                        session=info.context.session,
                        image_id=image.id,
                        image_class=CategoryImage,
                    ),
                    "filename": image.s3_filename,
                    "description": image.description,
                }
                for image in images
            ]

        return {
            "name": category_name,
            "ID": cat_id,
            # "description": "",
            "category_images": category_images,
        }

    # secret_place_extra_id = graphene.String()
    # user_marked_id = graphene.String()

    # async def resolve_user_marked_id(self, info):
    #     session: AsyncSession = info.context.session
    #     user_id = (
    #         (
    #             await session.execute(
    #                 sa.select(M2MUserPlaceMarked.user_id).where(
    #                     M2MUserPlaceMarked.place_id == self.id
    #                 )
    #             )
    #         )
    #         .fetchone()
    #         .user_id
    #     )
    #     return encode_gql_id("UserType", user_id)

    # TODO Refactor this piece of shit
    async def resolve_images(self, info):
        session: AsyncSession = info.context.session
        images = (
            await session.execute(
                sa.select(PlaceImage.id).where(PlaceImage.place_id == self.id)
            )
        ).fetchall()
        result = [
            await get_presigned_url(
                session=info.context.session, image_id=image.id, image_class=PlaceImage
            )
            for image in images
        ]
        return result

    # todo places added by user
    # todo places visited by user
    # todo secret place opened by user
    # todo places favourited by user

    async def resolve_is_decaying(self, info):
        session: AsyncSession = info.context.session
        decay = (
            (
                await session.execute(
                    sa.select(Place.active_due_date).where(Place.id == self.id)
                )
            )
            .fetchone()
            .active_due_date
        )
        if not decay:
            return False
        return True

    async def resolve_has_decayed(self, info):
        session: AsyncSession = info.context.session
        decay = (
            (
                await session.execute(
                    sa.select(Place.active_due_date).where(Place.id == self.id)
                )
            )
            .fetchone()
            .active_due_date
        )
        if not decay:
            return False
        return (
            decay + datetime.timedelta(hours=s.PLACE_BURNOUT_DURATION_HOURS)
        ) < datetime.datetime.now()

    @classmethod
    async def set_select_from(cls, info, q, query_fields):
        session: AsyncSession = info.context.session
        asker_id = AuthChecker.check_auth_request(info)
        user_to_filter_place = info.variable_values.get("userOwner")
        if user_to_filter_place:
            user_to_filter_place = decode_gql_id(user_to_filter_place)[1]
        include_my_places = info.variable_values.get("includeMyPlaces", False)

        if not include_my_places:
            q = q.where(Place.owner_id != asker_id)
        if user_to_filter_place:
            q = q.where(Place.owner_id == user_to_filter_place)

        if not info.variable_values.get("showSecretPlaces"):
            q = q.select_from(
                sa.join(Place, Category, Place.category_id == Category.id)
            ).where(Category.name != s.SECRET_PLACE_NAME)
        if not info.variable_values.get("showDecayedPlaces"):
            future = datetime.datetime.now() + datetime.timedelta(minutes=9000)
            q = q.where(
                sa.sql.func.coalesce(Place.active_due_date, future)
                > datetime.datetime.now()
            )

        if "distanceFrom" in info.variable_values:
            if "longitudeFrom" and "latitudeFrom" not in info.variable_values:
                raise ValueError("Invalid request. Coordinates must be present")
            lat = info.variable_values["latitudeFrom"]
            long = info.variable_values["longitudeFrom"]
            dist = info.variable_values["distanceFrom"]

            delta_latitude = dist / 111  # 1 lat degree is roughly 111 km

            longitude_1_degree_length = 111.3 * math.cos(lat)
            delta_longitude = dist / longitude_1_degree_length
            q = q.where(
                sa.and_(
                    sa.func.ABS(Place.coordinate_longitude - long) < delta_longitude,
                    sa.func.ABS(Place.coordinate_latitude - lat) < delta_latitude,
                )
            )

        if "userFavourite" in info.variable_values:
            user_favourite = decode_gql_id(info.variable_values["userFavourite"])[1]
            q = q.outerjoin_from(
                Place,
                M2MUserPlaceFavourite,
                onclause=(Place.id == M2MUserPlaceFavourite.place_id),
            ).where(M2MUserPlaceFavourite.user_id == user_favourite)

        if "userVisited" in info.variable_values:
            user_visited = decode_gql_id(info.variable_values["userVisited"])[1]
            q = q.outerjoin_from(
                Place,
                M2MUserPlaceVisited,
                onclause=(Place.id == M2MUserPlaceVisited.place_id),
            ).where(M2MUserPlaceVisited.user_id == user_visited)

        return q

    async def resolve_owner_id(self, info):
        owner_id = encode_gql_id("UserType", self.id)
        return owner_id
