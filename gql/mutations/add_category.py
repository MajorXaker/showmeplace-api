from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields

from models.db_models import Category
from ..gql_types.category_type import CategoryType


class MutationAddCategory(SQLAlchemyCreateMutation):
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
