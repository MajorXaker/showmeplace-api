from typing import List, Type

import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyCreateMutation
from graphene import String
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models.images import PlaceImage, UserImage, CategoryImage
from utils.api_auth import AuthChecker
from utils.config import settings as s
from utils.hex_tools import encode_md5
from utils.s3_object_tools import (
    upload_to_s3_bucket,
    get_presigned_url,
    add_imagetype_routine,
)
from ..gql_id import decode_gql_id


# TODO receive b64s as dict, it would allow utilisation of extensions and image ordering
class MutationAddUserImage(SQLAlchemyCreateMutation):
    class Meta:
        model = PlaceImage
        arguments = {
            "user__id": graphene.ID(graphene.ID, required=True),
            "image__b64s": graphene.List(graphene.String, required=True),
        }

    images__presigned__urls = graphene.List(of_type=String)

    @classmethod
    async def mutate(cls, root, info, user__id: str, image__b64s: list):
        session: AsyncSession = info.context.session
        user_id = AuthChecker.check_auth_mutation(session=session, info=info)
        if len(image__b64s) > 1:
            raise ValueError("User images cannot be more than 1")
        file_extension = (
            ".jpg"  # TODO implement a feature to load images of diffrent types
        )
        user__id = decode_gql_id(user__id)[1]
        uploaded_images = (
            await add_imagetype_routine(
                extension=file_extension,
                image__b64s=image__b64s,
                entity_id=user__id,
                session=session,
                image_class=UserImage,  # WARNING might not work!
            )
        )[:1]
        await session.execute(
            sa.delete(UserImage).where(
                sa.and_(
                    UserImage.user_id == user__id,
                    UserImage.id != uploaded_images[0]["id"],
                )
            )
        )
        presigned_urls = [img["presigned_url"] for img in uploaded_images]
        return MutationAddUserImage(images__presigned__urls=presigned_urls)
