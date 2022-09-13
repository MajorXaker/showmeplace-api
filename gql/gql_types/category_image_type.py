from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode

from models.db_models import CategoryImage


class CategoryImageType(SQLAlchemyObjectType):
    class Meta:
        model = CategoryImage
        interfaces = (AsyncNode,)
        filter_fields = {
            CategoryImage.id: [OP_EQ, OP_IN],
        }
