from alchql import SQLAlchemyObjectType, gql_types
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode

from models.db_models import PlaceImage, CategoryImage, UserImage
from utils.s3_object_tools import get_presigned_url


class PlaceImageType(SQLAlchemyObjectType):
    class Meta:
        model = PlaceImage
        interfaces = (AsyncNode,)
        filter_fields = {
            PlaceImage.id: [OP_EQ, OP_IN],
            PlaceImage.place_id: [OP_EQ],
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


class CategoryImageType(SQLAlchemyObjectType):
    class Meta:
        model = CategoryImage
        interfaces = (AsyncNode,)
        filter_fields = {
            CategoryImage.id: [OP_EQ, OP_IN],
            CategoryImage.category_id: [OP_EQ],
            # Do not add any other filters, or it may cripple a presigned url resolver
        }
        only_fields = [
            CategoryImage.id.key,
            CategoryImage.category_id.key,
            CategoryImage.s3_path.key,
            CategoryImage.s3_filename.key,
            CategoryImage.description.key,
        ]

    presigned_url = gql_types.String()

    async def resolve_presigned_url(self, info):
        return await get_presigned_url(
            session=info.context.session, image_id=self.id, image_class=CategoryImage
        )


class UserImageType(SQLAlchemyObjectType):
    class Meta:
        model = UserImage
        interfaces = (AsyncNode,)
        filter_fields = {
            UserImage.id: [OP_EQ, OP_IN],
            UserImage.user_id: [OP_EQ],
            # Do not add any other filters, or it may cripple a presigned url resolver
        }
        only_fields = [
            UserImage.id.key,
            UserImage.user_id.key,
            UserImage.s3_path.key,
            UserImage.s3_filename.key,
            UserImage.description.key,
        ]

    presigned_url = gql_types.String()

    async def resolve_presigned_url(self, info):
        return await get_presigned_url(
            session=info.context.session, image_id=self.id, image_class=UserImage
        )
