import graphene
from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN, OP_ILIKE
from alchql.fields import ModelField
from alchql.node import AsyncNode
import sqlalchemy as sa

# from gql.utils.gql_id import encode_gql_id
from alchql.utils import FilterItem

from gql.gql_types.select_image_type import UserImageType
from models.db_models import User, Place
from models.db_models.m2m.m2m_user_place_marked import M2MUserPlaceMarked


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (AsyncNode,)
        filter_fields = {
            User.id: [OP_EQ, OP_IN],
            User.external_id: [OP_EQ],
            User.name: [OP_ILIKE],

            # Place.user_marked: [OP_EQ]
            # M2MUserFollowingUser.lead_id.key: [OP_EQ],
            # M2MUserFollowingUser.follower_id.key: [OP_EQ],
        }
        only_fields = [
            User.id.key,
            User.name.key,
            User.has_onboarded.key,
            User.level.key,
            User.coins.key,
            User.external_id.key,
            User.external_id_type.key,
        ]

        image = ModelField(
            UserImageType,
            model_field=Place.category_id,
        )
        #
        # async def set_select_from(cls, info, q, query_fields):
        #     aaa = q

        # TODO namee ilike
        # todo user - marked place
        # todo users - place visited
        # todo user - secret place openeer
        #

        # "name__ilike": FilterItem(
        #     field_type=graphene.String,
        #     filter_func=lambda x: sa.or_(
        #         User.uid == x,
        #         sa.func.to_tsvector(unaccent(m.Artist.name)).op("@@")(
        #             parse_query(unidecode(x))
        #         ),
        #     ),
        # ),

    # def resolve_id(self, info):
    #     return encode_gql_id(self.__class__.__name__, self.id)
