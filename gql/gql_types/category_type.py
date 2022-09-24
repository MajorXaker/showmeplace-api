from alchql import SQLAlchemyObjectType
from alchql.batching import get_batch_resolver
from alchql.fields import ModelField
from alchql.node import AsyncNode

from models.db_models import Place, Category


class CategoryType(SQLAlchemyObjectType):
    class Meta:
        model = Category
        interfaces = (AsyncNode,)

