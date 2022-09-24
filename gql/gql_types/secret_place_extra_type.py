from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ
from alchql.node import AsyncNode

from models.db_models import SecretPlaceExtra
from utils.api_auth import AuthChecker


class SecretPlaceExtraType(SQLAlchemyObjectType):
    class Meta:
        model = SecretPlaceExtra
        sort = None
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

    @classmethod
    async def set_select_from(cls, info, q, query_fields):
        asker_id = AuthChecker.check_auth_request(info)
        return q
