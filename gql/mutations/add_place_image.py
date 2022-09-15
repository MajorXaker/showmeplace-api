import graphene
from alchql import SQLAlchemyCreateMutation
from graphene import ObjectType, String, Field
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from models.db_models.images import PlaceImage
from utils.config import settings as s
from utils.hex_tools import encode_md5
from utils.s3_object_tools import upload_to_s3_bucket, get_presigned_url
from ..gql_id import decode_gql_id
from ..gql_types.place_image_type import PlaceImageType

# class ImagesURL(ObjectType):
#     presigned_url = String()
#
# class ImagesURLs(ObjectType):
#     images = graphene.List(of_type=ImagesURL)


# TODO receive b64s as dict, it would allow utilisation of extensions and image ordering
class MutationAddPlaceImage(SQLAlchemyCreateMutation):
    class Meta:
        model = PlaceImage
        # output = PlaceImageType
        arguments = {
            "place__id": graphene.ID(graphene.ID, required=True),
            "image__b64s": graphene.List(graphene.String, required=True),
        }

    images__presigned__urls = graphene.List(of_type=String)

    @classmethod
    async def mutate(cls, root, info, place__id: str, image__b64s: list):
        session: AsyncSession = info.context.session
        extension = ".jpg"  # TODO implement a feature to load images of diffrent types
        place__id = decode_gql_id(place__id)[1]
        presigned_urls = []
        for img in image__b64s:
            # TODO what if I get md5 of the whole picture and then put it here
            filename = encode_md5(f"UID{place__id}{img[:16]}UID")

            await upload_to_s3_bucket(
                fileobj=img,
                folder=s.S3_PLACE_IMAGE_BUCKET,
                filename=filename,
                extension=extension,
            )
            full_filename = f"{filename}{extension}"

            image_id_cursor = await session.execute(
                sa.insert(PlaceImage)
                .values(
                    {
                        PlaceImage.place_id: place__id,
                        PlaceImage.s3_path: s.S3_PLACE_IMAGE_BUCKET,
                        PlaceImage.s3_filename: full_filename,
                    }
                )
                .returning(PlaceImage.id)
            )
            image_id = image_id_cursor.fetchone().id
            presigned_url = await get_presigned_url(
                session=session, image_id=image_id, image_class=PlaceImage
            )
            presigned_urls.append(presigned_url)
        return MutationAddPlaceImage(images__presigned__urls=presigned_urls)

