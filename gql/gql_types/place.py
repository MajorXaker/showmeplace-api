import graphene
from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode
import sqlalchemy as sa

# from gql.utils.gql_id import encode_gql_id
from alchql.utils import FilterItem

from models.db_models import User, Place


class PlaceType(SQLAlchemyObjectType):
    class Meta:
        model = Place
        interfaces = (AsyncNode,)
        filter_fields = {
            Place.id: [OP_EQ, OP_IN],
            Place.category_id: [OP_EQ, OP_IN],
            # "name__ilike": FilterItem(
            #     field_type=graphene.String,
            #     filter_func=lambda x: sa.or_(
            #         User.uid == x,
            #         sa.func.to_tsvector(unaccent(m.Artist.name)).op("@@")(
            #             parse_query(unidecode(x))
            #         ),
            #     ),
            # ),
            # "distance": FilterItem(
            #     field_type=graphene.Int,
            #     filter_func=size_filter,
            # ),

        }
        only_fields = [
            Place.id.key,
            Place.name.key,
            Place.description.key,
            Place.coordinate_longitude,
            Place.coordinate_latitude,
            Place.category_id,
        ]


    # def resolve_id(self, info):
    #     return encode_gql_id(self.__class__.__name__, self.id)
    # def size_filter(v: Int):
    #     max_val = sa.func.greatest(
    #         m.Description.measurements_width_cm,
    #         m.Description.measurements_height_cm,
    #         m.Description.measurements_depth_cm,
    #         m.Description.measurements_diameter_cm,
    #     )
    #
    #     result = {
    #         SizeFilter.OTHER: max_val.is_(None),
    #         SizeFilter.SMALL: max_val < 50,
    #         SizeFilter.MEDIUM: sa.and_(max_val > 49, max_val < 100),
    #         SizeFilter.BIG: max_val > 99,
    #     }[v]
    #
    #     return result
