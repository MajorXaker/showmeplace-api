import graphene
from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode
import sqlalchemy as sa

# from gql.utils.gql_id import encode_gql_id
from alchql.utils import FilterItem

from models.db_models import User, M2MUserFollowingUser


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (AsyncNode,)
        filter_fields = {
            User.id: [OP_EQ, OP_IN],
            M2MUserFollowingUser.lead_id.key: [OP_EQ],
            M2MUserFollowingUser.follower_id.key: [OP_EQ],
            # "name__ilike": FilterItem(
            #     field_type=graphene.String,
            #     filter_func=lambda x: sa.or_(
            #         User.uid == x,
            #         sa.func.to_tsvector(unaccent(m.Artist.name)).op("@@")(
            #             parse_query(unidecode(x))
            #         ),
            #     ),
            # ),
        }
        only_fields = [
            User.id.key,
            User.name.key,
            User.has_onboarded,
            User.level,
            User.coins,
        ]

    # def resolve_id(self, info):
    #     return encode_gql_id(self.__class__.__name__, self.id)
