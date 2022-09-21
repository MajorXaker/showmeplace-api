from alchql import SQLAlchemyUpdateMutation
from alchql.get_input_type import get_input_fields

from gql.gql_types.user_type import UserType
from models.db_models import User
from utils.api_auth import AuthChecker


class MutationUpdateUser(SQLAlchemyUpdateMutation):
    class Meta:
        model = User
        input_fields = get_input_fields(
            model=User,
            exclude_fields=[User.coins.key],
        )
        output = UserType
        input_type_name = "InputUpdateUser"

    @classmethod
    async def mutate(cls, root, info, value: dict):
        user_id = AuthChecker.check_auth_mutation(
            session=info.context.session, info=info
        )
        result = await super().mutate(root, info, value)

        return result
