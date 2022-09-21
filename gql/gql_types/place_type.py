import math

import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyObjectType, gql_types
from alchql.consts import OP_EQ, OP_IN
from alchql.fields import ModelField
from alchql.node import AsyncNode
from alchql.utils import FilterItem
from graphene import ObjectType, String
from sqlalchemy.ext.asyncio import AsyncSession
from unidecode import unidecode

from gql.gql_id import decode_gql_id, encode_gql_id
from gql.gql_types.category_type import CategoryType, CatImage
from gql.gql_types.secret_place_extra_type import SecretPlaceExtraType
from gql.gql_types.select_image_type import PlaceImageType
from models.db_models import (
    Place,
    SecretPlaceExtra,
    M2MUserPlaceMarked,
    M2MUserPlaceFavourite,
    PlaceImage,
    User,
    Category,
    CategoryImage,
)
from models.db_models.m2m.m2m_user_place_visited import M2MUserPlaceVisited
from utils.api_auth import check_auth, AuthChecker

# from gql.utils.gql_id import encode_gql_id
from utils.pars_query import parse_query
from utils.s3_object_tools import get_presigned_url


class Cat(ObjectType):
    name = String()
    # filename = String()
    # description = String()
    category_images = graphene.List(of_type=CatImage)


class PlaceType(SQLAlchemyObjectType):
    class Meta:
        filter_fields = {
            Place.id: [OP_EQ, OP_IN],
            Place.category_id: [OP_EQ, OP_IN],
            "latitude__from": FilterItem(field_type=graphene.Float, filter_func=None),
            "longitude__from": FilterItem(field_type=graphene.Float, filter_func=None),
            "distance__from": FilterItem(field_type=graphene.Float, filter_func=None),
            "include__my__places": FilterItem(
                field_type=graphene.Boolean, filter_func=None
            ),
            "user__marked": FilterItem(field_type=graphene.String, filter_func=None),
            "user__favourite": FilterItem(field_type=graphene.String, filter_func=None),
            "user__visited": FilterItem(field_type=graphene.String, filter_func=None),
            "name__ilike": FilterItem(
                field_type=graphene.String,
                filter_func=lambda x: sa.func.to_tsvector(Place.name).op("@@")(
                    parse_query(unidecode(x))
                ),
            ),
        }

        model = Place
        interfaces = (AsyncNode,)
        only_fields = [
            Place.id.key,
            Place.name.key,
            Place.description.key,
            Place.coordinate_longitude.key,
            Place.coordinate_latitude.key,
            # Place.category_id.key,
        ]

    category_data = graphene.Field(type_=Cat)

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

    # category_id = graphene.String()
    # category_name = graphene.String()
    images = graphene.List(of_type=graphene.String)
    # secret_place_extra_id = graphene.String()
    user_marked_id = graphene.String()

    # async def resolve_category_images(self, info):
    #     session: AsyncSession = info.context.session
    #     images = (
    #         await session.execute(
    #             sa.select(
    #                 CategoryImage.id,
    #                 CategoryImage.s3_filename,
    #                 CategoryImage.description,
    #             ).where(CategoryImage.category_id == self.category_id)
    #         )
    #     ).fetchall()
    #     result = [
    #         {
    #             "presigned_url": await get_presigned_url(
    #                 session=info.context.session,
    #                 image_id=image.id,
    #                 image_class=CategoryImage,
    #             ),
    #             "filename": image.s3_filename,
    #             "description": image.description,
    #         }
    #         for image in images
    #     ]
    #     return result

    async def resolve_user_marked_id(self, info):
        session: AsyncSession = info.context.session
        user_id = (
            (
                await session.execute(
                    sa.select(M2MUserPlaceMarked.user_id).where(
                        M2MUserPlaceMarked.place_id == self.id
                    )
                )
            )
            .fetchone()
            .user_id
        )
        return encode_gql_id("UserType", user_id)

    # async def resolve_category(self, info):

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

    # async def resolve_secret_place_extra_id(self, info):
    #     session: AsyncSession = info.context.session
    #
    #     return encode_gql_id("SecretPlaceExtraType", self.category_id)

    # is_secret_place_opened = gql_types.Boolean()
    # secret_place_extra = ModelField(
    #     SecretPlaceExtraType,
    #     model_field=SecretPlaceExtra.place_id,
    # )
    # place_category = ModelField(
    #     CategoryType,
    #     model_field=Place.category_id,
    # )
    # image = ModelField(
    #     PlaceImageType,
    #     model_field=Place.category_id,
    # )

    # todo places added by user
    # todo places visited by user
    # todo secret place opened by user
    # todo places favourited by user

    # async def resolve_is_secret_place_opened(self, info):
    #     # TODO LOGIC
    #     return True

    @classmethod
    async def set_select_from(cls, info, q, query_fields):
        asker_id = AuthChecker.check_auth_request(info)

        user_to_filter_place = decode_gql_id(info.variable_values.get("userMarked"))[1]
        include_my_places = info.variable_values.get("includeMyPlaces", False)

        q = cls.user_marked_logic(
            query=q,
            asker_id=asker_id,
            user_to_filter_place=user_to_filter_place,
            include_my_places=include_my_places,
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

        q = await cls.user_marked_logic(info, q)

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

    @staticmethod
    def user_marked_logic(
        query,
        asker_id: int,
        user_to_filter_place: int | None = None,
        include_my_places: bool = False,
    ):

        query = query.outerjoin_from(
            Place,
            M2MUserPlaceMarked,
            onclause=(Place.id == M2MUserPlaceMarked.place_id),
        )
        if user_to_filter_place:
            query = query.where(M2MUserPlaceMarked.user_id == user_to_filter_place)
        if include_my_places:
            query = query.where(M2MUserPlaceMarked.user_id == asker_id)
        return query

    # def resolve_category_id(self, info):
    #     return encode_gql_id(self.__class__.__name__, self.category_id)
