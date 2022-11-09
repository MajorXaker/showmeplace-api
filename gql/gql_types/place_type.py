import datetime
import math

import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode
from alchql.utils import FilterItem
from graphene import ObjectType, String, Float
from sqlalchemy.ext.asyncio import AsyncSession
from unidecode import unidecode

from gql.gql_id import decode_gql_id, encode_gql_id
from gql.gql_types.category_type import CatImage
from models.db_models import (
    Place,
    M2MUserPlaceFavourite,
    PlaceImage,
    Category,
    CategoryImage,
    M2MUserOpenedSecretPlace,
    SecretPlaceExtra,
)
from models.db_models.m2m.m2m_user_place_visited import M2MUserPlaceVisited
from models.enums import SecretPlacesFilterEnum, DecayingPlacesFilterEnum
from utils.api_auth import AuthChecker
from utils.config import settings as s
from utils.filters import (
    secrets_filter,
    decaying_filter,
    box_coordinates_filter,
    decaying_filter_list,
)
from utils.logging_tools import debug_log
from utils.pars_query import parse_query
from utils.s3_object_tools import get_presigned_url
from utils.smp_exceptions import ExceptionGroupEnum, Exc, ExceptionReasonEnum
from utils.utils import CountableConnectionCreator


class Cat(ObjectType):
    name = String()
    mark = String()
    id = String()
    category_images = graphene.List(of_type=CatImage)


class SecretPlaceExtraObject(ObjectType):
    id = String()
    food_suggestion = String()
    time_suggestion = String()
    company_suggestion = String()
    music_suggestion = String()
    extra_suggestion = String()


class CoordinateBox(graphene.InputObjectType):
    ne_longitude = Float()
    ne_latitude = Float()
    sw_longitude = Float()
    sw_latitude = Float()


class PlaceType(SQLAlchemyObjectType):
    class Meta:
        model = Place
        interfaces = (AsyncNode,)
        connection_class = CountableConnectionCreator
        filter_fields = {
            Place.id: [OP_EQ, OP_IN],
            Place.category_id: [OP_EQ, OP_IN],
            # "coordinate_box": CoordinateBox(),
            "coordinate_box": FilterItem(
                field_type=CoordinateBox, filter_func=box_coordinates_filter
            ),
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
            "secrets_filter": FilterItem(
                field_type=graphene.Enum.from_enum(SecretPlacesFilterEnum),
                filter_func=secrets_filter,
            ),
            "decay_filter": FilterItem(
                field_type=graphene.Enum.from_enum(DecayingPlacesFilterEnum),
                filter_func=decaying_filter,
            ),
            "decay_filter_list": FilterItem(
                field_type=graphene.List(
                    of_type=graphene.Enum.from_enum(DecayingPlacesFilterEnum)
                ),
                filter_func=decaying_filter_list,
            ),
            "opened_secret_places": FilterItem(
                field_type=graphene.Boolean, filter_func=None
            ),
        }

        only_fields = [
            Place.id.key,
            Place.name.key,
            Place.description.key,
            Place.coordinate_longitude.key,
            Place.coordinate_latitude.key,
            Place.active_due_date.key,
            Place.address.key,
        ]

    secret_extra_field = graphene.Field(type_=SecretPlaceExtraObject)
    category_data = graphene.Field(type_=Cat)
    images = graphene.List(of_type=graphene.String)
    is_decaying = graphene.Boolean()
    has_decayed = graphene.Boolean()
    owner_id = graphene.String()
    has_visited = graphene.Boolean()
    has_favourited = graphene.Boolean()
    is_opened_for_user = graphene.Boolean()

    async def resolve_secret_extra_field(self, info):
        session: AsyncSession = info.context.session
        extra = (
            await session.execute(
                sa.select(
                    SecretPlaceExtra.id,
                    SecretPlaceExtra.food_suggestion,
                    SecretPlaceExtra.extra_suggestion,
                    SecretPlaceExtra.music_suggestion,
                    SecretPlaceExtra.time_suggestion,
                    SecretPlaceExtra.company_suggestion,
                )
                .select_from(
                    sa.join(
                        Place,
                        SecretPlaceExtra,
                        SecretPlaceExtra.id == Place.secret_extra_id,
                    )
                )
                .where(Place.secret_extra_id == self.id)
            )
        ).fetchone()
        if not extra:
            return None
        data = dict(extra)
        data["id"] = encode_gql_id("SecretPlaceType", data["id"])
        return data

    async def resolve_category_data(self, info):
        session: AsyncSession = info.context.session

        category = (
            await session.execute(
                sa.select(Place.category_id, Category.name, Category.mark)
                .join(Category, Place.category_id == Category.id)
                .where(Place.id == self.id)
            )
        ).fetchone()

        coded_id = encode_gql_id(
            "CategoryType",
            category.category_id,
        )

        images = (
            await session.execute(
                sa.select(
                    CategoryImage.id,
                    CategoryImage.s3_filename,
                    CategoryImage.description,
                ).where(CategoryImage.category_id == category.category_id)
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
            "name": category.name,
            "id": coded_id,
            "mark": category.mark,
            "category_images": category_images,
        }

    # secret_place_extra_id = graphene.String()

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

    @classmethod
    async def set_select_from(cls, info, q, query_fields):

        await debug_log(cls, info)

        session: AsyncSession = info.context.session
        asker_id = AuthChecker.check_auth_request(info)
        user_owner = info.variable_values.get("userOwner")
        if user_owner:
            user_owner = decode_gql_id(user_owner)[1]
        include_my_places = info.variable_values.get("includeMyPlaces", False)

        # M2MUserOpenedSecretPlace.user_id == asker_id))
        if not include_my_places:
            q = q.where(Place.owner_id != asker_id)
        if user_owner:
            q = q.where(Place.owner_id == user_owner)

        if "distanceFrom" in info.variable_values:
            if (
                "longitudeFrom" not in info.variable_values
                or "latitudeFrom" not in info.variable_values
            ):
                Exc.missing_data(
                    message="No user coordinates provided",
                    of_group=ExceptionGroupEnum.COORDINATES,
                    reasons=ExceptionReasonEnum.MISSING_VALUE,
                )
            lat = info.variable_values["latitudeFrom"]
            long = info.variable_values["longitudeFrom"]
            dist = info.variable_values["distanceFrom"]

            delta_latitude = abs(dist / 111)  # 1 lat degree is roughly 111 km

            longitude_1_degree_length = abs(111.3 * math.cos(lat))
            delta_longitude = dist / longitude_1_degree_length
            q = q.where(
                sa.and_(
                    sa.func.ABS(Place.coordinate_longitude - long) < delta_longitude,
                    sa.func.ABS(Place.coordinate_latitude - lat) < delta_latitude,
                )
            )

        has_opened = info.variable_values.get("openedSecretPlaces", False)
        if has_opened:
            q = (
                q.outerjoin_from(
                    Place,
                    M2MUserOpenedSecretPlace,
                    onclause=(Place.id == M2MUserOpenedSecretPlace.place_id),
                )
                .join(Category, Place.category_id == Category.id)
                .where(
                    sa.or_(
                        Category.mark != "secret",
                        M2MUserOpenedSecretPlace.user_id == asker_id,
                    )
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

    async def resolve_has_favourited(self, info):
        asker_id = AuthChecker.check_auth_request(info)
        session: AsyncSession = info.context.session
        visit = (
            await session.execute(
                sa.select(M2MUserPlaceFavourite).where(
                    M2MUserPlaceFavourite.place_id == self.id,
                    M2MUserPlaceFavourite.user_id == asker_id,
                )
            )
        ).fetchone()
        return True if visit else False

    async def resolve_has_visited(self, info):
        asker_id = AuthChecker.check_auth_request(info)
        session: AsyncSession = info.context.session
        visit = (
            await session.execute(
                sa.select(M2MUserPlaceVisited).where(
                    M2MUserPlaceVisited.place_id == self.id,
                    M2MUserPlaceVisited.user_id == asker_id,
                )
            )
        ).fetchone()
        return True if visit else False

    async def resolve_is_opened_for_user(self, info):
        asker_id = AuthChecker.check_auth_request(info)
        session: AsyncSession = info.context.session
        is_secret = (
            await session.execute(
                sa.select(Category.id, Category.mark, Place.owner_id)
                .join(Place, Place.category_id == Category.id)
                .where(Place.id == self.id)
            )
        ).fetchone()
        if is_secret:
            if not is_secret.mark or is_secret.owner_id == asker_id:
                return True
        visit = (
            await session.execute(
                sa.select(M2MUserOpenedSecretPlace)
                .join(Place, Place.id == M2MUserOpenedSecretPlace.place_id)
                .where(
                    M2MUserOpenedSecretPlace.place_id == self.id,
                    M2MUserOpenedSecretPlace.user_id == asker_id,
                )
            )
        ).fetchone()
        return True if visit else False

    async def resolve_is_decaying(self, info):
        session: AsyncSession = info.context.session
        decay = (
            (
                await session.execute(
                    sa.select(Place.active_due_date).where(
                        sa.and_(
                            Place.id == self.id,
                        ),
                    )
                )
            )
            .fetchone()
            .active_due_date
        )
        if not decay:
            return False
        return decay > datetime.datetime.now()

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
            decay + datetime.timedelta(hours=s.PLACE_DECAY_DURATION_HOURS)
        ) < datetime.datetime.now()

    async def resolve_owner_id(self, info):
        session: AsyncSession = info.context.session
        place = (
            await session.execute(sa.select(Place.owner_id).where(Place.id == self.id))
        ).fetchone()
        owner_id_encoded = encode_gql_id("UserType", place.owner_id)
        return owner_id_encoded
