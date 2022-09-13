from alchql import SQLAlchemyDeleteMutation
from alchql.get_input_type import get_input_fields

from models.db_models import Category
from ..gql_types.category_type import PlaceCategoryType


class MutationRemoveCategory(SQLAlchemyDeleteMutation):
    class Meta:
        model = Category
        output = PlaceCategoryType
        input_fields = get_input_fields(
            model=Category,
            only_fields=[
                Category.name.key,
            ],
            required_fields=[Category.name.key],
        )

    # @classmethod
    # async def mutate(cls, root, info, value: dict):
    #
    #     result = await super().mutate(root, info, value)
    #
    #
    #     return result
