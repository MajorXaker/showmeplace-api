from alchql import SQLAlchemyUpdateMutation
from alchql.get_input_type import get_input_fields

from models.db_models import Category
from utils.api_auth import AuthChecker
from ..gql_types.category_type import CategoryType


class MutationUpdateCategory(SQLAlchemyUpdateMutation):
    class Meta:
        model = Category
        output = CategoryType
        input_fields = get_input_fields(
            model=Category,
            only_fields=[
                Category.name.key,
            ],
            required_fields=[Category.name.key],
        )

    @classmethod
    async def mutate(cls, root, info, value: dict):
        user_id = await AuthChecker.check_auth_mutation(
            session=info.context.session, info=info
        )
        result = await super().mutate(root, info, value)

        return result
