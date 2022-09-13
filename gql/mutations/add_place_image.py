import graphene
from alchql import SQLAlchemyCreateMutation
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from models.db_models.images import PlaceImage
from utils.config import settings as s
from utils.hex_tools import encode_md5
from utils.s3_object_tools import AWSS3Tools, upload_to_s3_bucket
from ..gql_types.place_image_type import PlaceImageType


# TODO receive b64s as dict, it would allow utilisation of extensions and image ordering
class MutationAddPlaceImage(SQLAlchemyCreateMutation):
    class Meta:
        model = PlaceImage
        output = PlaceImageType
        arguments = {
            "place__id": graphene.ID(graphene.ID, required=True),
            "image__b64s": graphene.List(graphene.String, required=True),
        }

    @classmethod
    async def mutate(cls, root, info, place__id: str, image__b64s: list):
        session: AsyncSession = info.context.session
        extension = ".jpg" # TODO implement a feature to load images of diffrent types
        for img in image__b64s:
            filename = encode_md5(f"UID{place__id}{img[:16]}UID")

            await upload_to_s3_bucket(
                fileobj=img,
                folder=s.S3_PLACE_IMAGE_BUCKET,
                filename=filename,
                extension=extension,
            )
            full_filename = f"{filename}{extension}"
            await session.execute(
                sa.insert(PlaceImage).values(
                    {
                        PlaceImage.place_id: place__id, # check whether in needs 64debasing
                        PlaceImage.s3_path: s.S3_PLACE_IMAGE_BUCKET,
                        PlaceImage.s3_filename: full_filename,

                    }
                )
            )
            # await AWSS3Tools.get_presigned_url()



        # create all necessary data - presigned url + its date + put file into s3
        # then create rows in place_image table with theese data

        # return result
