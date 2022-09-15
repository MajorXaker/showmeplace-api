from alchql import SQLAlchemyObjectType, gql_types
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode

from models.db_models import PlaceImage
from utils.s3_object_tools import get_presigned_url


class PlaceImageType(SQLAlchemyObjectType):
    class Meta:
        model = PlaceImage
        interfaces = (AsyncNode,)
        filter_fields = {
            PlaceImage.id: [OP_EQ, OP_IN],
            PlaceImage.place_id:[OP_EQ],
            # Do not add any other filters, or it may cripple a presigned url resolver
        }
        only_fields = [
            PlaceImage.id.key,
            PlaceImage.place_id.key,
            PlaceImage.s3_path.key,
            PlaceImage.s3_filename.key,
            PlaceImage.description.key,
        ]

    presigned_url = gql_types.String()

    async def resolve_presigned_url(self, info):
        return await get_presigned_url(
            session=info.context.session, image_id=self.id, image_class=PlaceImage
        )
