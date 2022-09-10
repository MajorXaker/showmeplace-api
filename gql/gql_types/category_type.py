from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode

from models.db_models import PlaceCategory


class PlaceCategoryType(SQLAlchemyObjectType):
    class Meta:
        model = PlaceCategory
        interfaces = (AsyncNode,)
        filter_fields = {
            PlaceCategory.id: [OP_EQ, OP_IN],
        }
