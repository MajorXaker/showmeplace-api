import graphene
from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN, OP_ILIKE
from alchql.node import AsyncNode
import sqlalchemy as sa

# from gql.utils.gql_id import encode_gql_id
from alchql.utils import FilterItem

from models.db_models import User, Place, SecretPlaceExtra
from models.db_models.m2m.m2m_user_place_marked import M2MUserPlaceMarked


class SecretPlaceExtraType(SQLAlchemyObjectType):
    class Meta:
        model = SecretPlaceExtra
        interfaces = (AsyncNode,)
        filter_fields = {
            SecretPlaceExtra.id: [OP_EQ],
            SecretPlaceExtra.place_id: [OP_EQ],
        }
        only_fields = [
            SecretPlaceExtra.id.key,
            SecretPlaceExtra.food_suggestion.key,
            SecretPlaceExtra.time_suggestion.key,
            SecretPlaceExtra.company_suggestion.key,
            SecretPlaceExtra.music_suggestion.key,
            SecretPlaceExtra.extra_suggestion.key,
        ]
