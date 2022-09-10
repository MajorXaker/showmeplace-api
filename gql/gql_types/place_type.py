from alchql import SQLAlchemyObjectType, gql_types
from alchql.consts import OP_EQ, OP_IN, OP_ILIKE
from alchql.fields import ModelField
from alchql.node import AsyncNode

from gql.gql_types.category_type import PlaceCategoryType
from gql.gql_types.secret_place_extra_type import SecretPlaceExtraType
from models.db_models import Place


# from gql.utils.gql_id import encode_gql_id


class PlaceType(SQLAlchemyObjectType):
    class Meta:
        model = Place
        interfaces = (AsyncNode,)
        filter_fields = {
            Place.id: [OP_EQ, OP_IN],
            Place.category_id: [OP_EQ, OP_IN],
            Place.name: [OP_ILIKE]
            # TODO namee ilike
            # todo places added by user
            # todo places visited by user
            # todo secret place opened by user
            # todo places favouritted by user
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
            Place.coordinate_longitude.key,
            Place.coordinate_latitude.key,
        ]

    is_secret_place_opened = gql_types.Boolean()
    secret_place_extra = ModelField(
        SecretPlaceExtraType,
        model_field=Place.secret_place_extra_id,
    )
    place_category = ModelField(
        PlaceCategoryType,
        model_field=Place.category_id,
    )

    async def resolve_is_secret_place_opened(self, info):
        # TODO LOGIC
        return True

    async def resolve_secret_place_extra(self, info):
        # TODO LOGIC
        pass

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
