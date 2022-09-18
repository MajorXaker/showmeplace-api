import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN
from alchql.fields import ModelField
from alchql.node import AsyncNode
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_types.select_image_type import CategoryImageType
from models.db_models import Category, CategoryImage
from utils.s3_object_tools import get_presigned_url


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
        only_fields = [Category.id, Category.name]
        images = graphene.List(of_type=graphene.String)

        async def resolve_images(self, info):
            session: AsyncSession = info.context.session
            images = (
                await session.execute(
                    sa.select(CategoryImage.id).where(CategoryImage.place_id == self.id)
                )
            ).fetchall()
            result = [
                await get_presigned_url(
                    session=info.context.session,
                    image_id=image.id,
                    image_class=CategoryImage,
                )
                for image in images
            ]
            return result
