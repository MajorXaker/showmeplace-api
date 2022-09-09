# import api_models.models as m
import sqlalchemy as sa
from alchql import SQLAlchemyUpdateMutation

from gql.gql_types.user_type import UserType
from models.db_models import User


from alchql.get_input_type import get_input_fields
from alchql.gql_id import ResolvedGlobalId
from sqlalchemy.ext.asyncio import AsyncSession

#
# from auth.retool_user import is_retool_user
# from gql.exceptions import Forbidden
# from gql.gql_types import LotType
# from gql.utils.recalculate_prices import recalculate_prices
# from gql.utils.update_artwork_last_sold_data import update_artwork_last_sold_data


class MutationUpdateUser(SQLAlchemyUpdateMutation):
    class Meta:
        model = User
        input_fields = get_input_fields(
            model=User,
            exclude_fields=[User.coins.key],
        )
        output = UserType
        input_type_name = "InputUpdateUser"

    # @classmethod
    # async def mutate(cls, root, info, id, value):
    #
    #
    #     result = await super().mutate(root, info, id, value)
    #
    #     return result
