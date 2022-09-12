from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode

from models.db_models.place_image import PlaceImage


class PlaceImageType(SQLAlchemyObjectType):
    class Meta:
        model = PlaceImage
        interfaces = (AsyncNode,)
        filter_fields = {
            PlaceImage.id: [OP_EQ, OP_IN],
        }
