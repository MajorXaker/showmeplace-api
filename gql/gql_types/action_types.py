from alchql import SQLAlchemyObjectType
from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN, OP_ILIKE
from alchql.node import AsyncNode

from models.db_models import ActionsEconomy
from utils.api_auth import AuthChecker


class ActionType(SQLAlchemyObjectType):
    class Meta:
        model = ActionsEconomy
        interfaces = (AsyncNode,)
        filter_fields = {
            ActionsEconomy.id: [OP_EQ, OP_IN],
            ActionsEconomy.action_name: [OP_ILIKE],
        }
        only_fields = [
            ActionsEconomy.id.key,
            ActionsEconomy.action_name.key,
            ActionsEconomy.description.key,
            ActionsEconomy.change_amount.key,
            ActionsEconomy.change_type.key,
        ]

    @classmethod
    async def set_select_from(cls, info, q, query_fields):
        asker_id = AuthChecker.check_auth_request(info)
        return q
