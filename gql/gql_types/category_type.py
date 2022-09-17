from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN
from alchql.fields import ModelField
from alchql.node import AsyncNode

from gql.gql_types.select_image_type import CategoryImageType
from models.db_models import Category


class CategoryType(SQLAlchemyObjectType):
    class Meta:
        model = Category
        interfaces = (AsyncNode,)
        filter_fields = {
            Category.id: [OP_EQ, OP_IN],
        }
        image = ModelField(
            CategoryImageType,
            model_field=Category.id,
        )
