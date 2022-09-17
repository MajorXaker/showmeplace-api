import math

import graphene
from alchql import SQLAlchemyObjectType, gql_types
from alchql.consts import OP_EQ, OP_IN, OP_ILIKE
from alchql.fields import ModelField
from alchql.node import AsyncNode
from alchql.utils import FilterItem
import sqlalchemy as sa
from unidecode import unidecode

from gql.gql_id import decode_gql_id
from gql.gql_types.category_type import CategoryType
from gql.gql_types.select_image_type import PlaceImageType
from gql.gql_types.secret_place_extra_type import SecretPlaceExtraType
from models.db_models import (
    Place,
    SecretPlaceExtra,
    M2MUserPlaceMarked,
    M2MUserPlaceFavourite,
)
from models.db_models.m2m.m2m_user_place_visited import M2MUserPlaceVisited

# from gql.utils.gql_id import encode_gql_id
from utils.pars_query import parse_query


class PlaceType(SQLAlchemyObjectType):
    class Meta:
        filter_fields = {
            Place.id: [OP_EQ, OP_IN],
            Place.category_id: [OP_EQ, OP_IN],
            # "latitude__from": FilterItem(field_type=graphene.Float, filter_func=None),
            # "longitude__from": FilterItem(field_type=graphene.Float, filter_func=None),
            # "distance__from": FilterItem(field_type=graphene.Float, filter_func=None),
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
        ]

    is_secret_place_opened = gql_types.Boolean()
    secret_place_extra = ModelField(
        SecretPlaceExtraType,
        model_field=SecretPlaceExtra.place_id,
    )
    place_category = ModelField(
        CategoryType,
        model_field=Place.category_id,
    )
    image = ModelField(
        PlaceImageType,
        model_field=Place.category_id,
    )

    # todo places added by user
    # todo places visited by user
    # todo secret place opened by user
    # todo places favourited by user

    # async def resolve_is_secret_place_opened(self, info):
    #     # TODO LOGIC
    #     return True

    # TODO Doesn't work. Need to find another way
    # TODO do it through new InputType
    # TODO Add hemishpere to models
    @classmethod
    async def set_select_from(cls, info, q, query_fields):
        # if "distanceFrom" in info.variable_values:
        #     if "longitudeFrom" and "latitudeFrom" not in info.variable_values:
        #         raise ValueError("Invalid request. Coordinates must be present")
        #     lat = info.variable_values["latitudeFrom"]
        #     long = info.variable_values["longitudeFrom"]
        #     dist = info.variable_values["distanceFrom"]
        #
        #     delta_latitude = dist / 111  # 1 lat degree is roughly 111 km
        #
        #     longitude_1_degree_length = 111.3 + math.cos(lat)
        #     delta_longitude = dist / longitude_1_degree_length
        #
        #     q = q.where(
        #         sa.and_(
        #             # for south hemisphere
        #             Place.coordinate_latitude.between(
        #                 lat + delta_latitude, lat - delta_latitude
        #             ),
        #             Place.coordinate_longitude.between(
        #                 long + delta_longitude, long - delta_longitude
        #             ),
        #             # for north hemisphere
        #             Place.coordinate_latitude.between(
        #                 lat + delta_latitude, lat - delta_latitude
        #             ),
        #             Place.coordinate_longitude.between(
        #                 long + delta_longitude, long - delta_longitude
        #             )
        #         )
        #     )

        if "userMarked" in info.variable_values:
            user_marked = decode_gql_id(info.variable_values["userMarked"])[1]
            q = q.outerjoin_from(
                Place,
                M2MUserPlaceMarked,
                onclause=(Place.id == M2MUserPlaceMarked.place_id),
            ).where(M2MUserPlaceMarked.user_id == user_marked)

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

    # def resolve_id(self, info):
    #     return encode_gql_id(self.__class__.__name__, self.id)
