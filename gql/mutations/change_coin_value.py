import graphene
from alchql import SQLAlchemyUpdateMutation
from alchql.get_input_type import get_input_fields
from alchql.gql_id import ResolvedGlobalId

import sqlalchemy as sa

from gql.gql_types.user import UserType
from models.db_models import User
from models.enums import CoinChange


class MutationChangeCoinValue(SQLAlchemyUpdateMutation):
    class Meta:
        model = User
        output = UserType
        input_fields = get_input_fields(model=User, only_fields=[User.id.key,],) | {
            "change_type": graphene.Enum.from_enum(CoinChange)(),
            "amount": graphene.Int(),
        }

    @classmethod
    async def mutate(cls, root, info, id: str, value: dict):
        query = sa.select(User.coins).scalar()
        session = info.context.session
        current_value = await session.execute(query)

        if value["change_type"] == CoinChange.INCREASE:
            new_value = current_value + value["amount"]
        else:
            new_value = current_value - value["amount"]

        if new_value < 0:
            new_value = 0
        value['coins'] = new_value

        result = await super().mutate(root, info, id, value)

        return result
