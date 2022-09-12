from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode

from models.db_models.user_image import UserImage


class UserImageType(SQLAlchemyObjectType):
    class Meta:
        model = UserImage
        interfaces = (AsyncNode,)
        filter_fields = {
            UserImage.id: [OP_EQ, OP_IN],
        }
