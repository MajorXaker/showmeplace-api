from alchql import SQLAlchemyUpdateMutation
from alchql.get_input_type import get_input_fields

from models.db_models import User, PlaceCategory
from ..gql_types.category_type import PlaceCategoryType


class MutationUpdateCategory(SQLAlchemyUpdateMutation):
    class Meta:
        model = PlaceCategory
        output = PlaceCategoryType
        input_fields = get_input_fields(
            model=PlaceCategory,
            only_fields=[
                PlaceCategory.name.key,
            ],
            required_fields=[PlaceCategory.name.key],
        )

    # @classmethod
    # async def mutate(cls, root, info, value: dict):
    #
    #     result = await super().mutate(root, info, value)
    #
    #
    #     return result
