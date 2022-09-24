import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN
from alchql.node import AsyncNode
from graphene import ObjectType, String
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models import Category, CategoryImage
from utils.api_auth import AuthChecker
from utils.s3_object_tools import get_presigned_url


class CatImage(ObjectType):
    presigned_url = String()
    filename = String()
    description = String()
#
#
# class OldCategoryType(SQLAlchemyObjectType):
#     class Meta:
#         model = Category
#         interfaces = (AsyncNode,)
#         filter_fields = {
#             Category.id: [OP_EQ, OP_IN],
#         }
#         only_fields = [Category.id.key, Category.name.key, Category.mark.key]
#
#     images = graphene.List(of_type=CatImage)
#
#     async def resolve_images(self, info):
#         session: AsyncSession = info.context.session
#         images = (
#             await session.execute(
#                 sa.select(
#                     CategoryImage.id,
#                     CategoryImage.s3_filename,
#                     CategoryImage.description,
#                 ).where(CategoryImage.category_id == self.id)
#             )
#         ).fetchall()
#         result = [
#             {
#                 "presigned_url": await get_presigned_url(
#                     session=info.context.session,
#                     image_id=image.id,
#                     image_class=CategoryImage,
#                 ),
#                 "filename": image.s3_filename,
#                 "description": image.description,
#             }
#             for image in images
#         ]
#         return result
#
#     @classmethod
#     async def set_select_from(cls, info, q, query_fields):
#         asker_id = AuthChecker.check_auth_request(info)
#         return q
