import base64
import datetime
from io import BytesIO
from typing import List, Type, Dict

import boto3
import sqlalchemy as sa
from botocore.exceptions import ClientError
from sqlalchemy.ext.asyncio import AsyncSession
from yarl import URL

from gql.gql_id import decode_gql_id
from models.db_models import PlaceImage, UserImage, CategoryImage
from utils.config import settings as s
from utils.hex_tools import encode_md5


# sample_img = "iVBORw0KGgoAAAANSUhEUgAAAH4AAAAsCAMAAACUu/xGAAAAq1BMVEUAAABlZVJlZVKsrJthYU+zs6Grq5ylpZazs6FlZVJfX01lZVJlZVKsrJurq5urq5xlZVKtrZ1lZVJlZVKvr52zs6GysqCoqJeqqpmzs6Grq5xlZVJgYE6zs6Gnp5mrq5yiopRjY1CRkX2rq5yzs6FlZVKRkX2goJKKineRkX2Pj3yrq5yIiHWRkX2RkX2RkX1lZVKRkX2rq5yzs6GoqJdfX02goJKHh3SHh3VrpzVsAAAAMHRSTlMAQIDHx3+Ax0Ag7qBgIA9AEFCPMLOgMO7bYKBQ24+zYNuzkY9wcAXu0oiocPFBMHYlVbK0AAAD3UlEQVRYw6SW7Y6qMBCGB0IkLfKdnB9ocFmjru7HERL03P+VnXY6bdmWjcF9f2inxjydvjMDcHy99zP693oEpTpQYjBR7W4VmzA81GoZCDn/ycrValVmYOJcKBWL1/4HnUEpupLGxOI47iQmDkfc4GEBEFyNQkClzYDKQQs3VmJBufu6G7zRWNMeUzEHUnLVWs/gy9vg4NNB4wUIPOG2h7e8NcV0HRt7QPDxfzTd4ptleB5F6ro3NtsIc7UnjMKKXyuN30ZS+PuLRMW7PN+l2vlhAZ6yqCZmcrm05stfOrwVpvEBaJWStIOpVk/gC8Rb62tjRj25Fx/fEsgqE27cluKB8GR9hDFzeX44CFbmJb9/Cn8w1ldA5tO9VD/gc8FpveTbxfi1LXWOl10Z80c0Yx7/jpyyjRtd9zuxU8ZL8FEYJjZFpg6yIfOpKsf1FJ+EUkzddKkabQ+o0zCcwMN/vZm+uLh4UmW7nptTCBVq5nUF4Y0CgBaNVip18jsPn370909cfX708/gusF3fkQfrKZHXHh45Wi8meRefvfVCfwGOZ9zx8TZ9TjWY2M6vVf4jm8e3WYrDJ1Vj4N3FHwVd6vKFCxefBMFmq7ub6UI7TMZw0SEv8ryPDVaoxPiWufhL/02zY0cm3ZH1VgxIIYa1U/nIibH/EZjjp4M/9w/x9FijbyuqdzOVH+BbWQJxHMupd4pjINhDPKVH1lslBl9g6OKb73j0wmoBHrMj691nsJ0QLn4l0/09nrIm6wv7nGdQqwjGucvPJSWjN4z8aXyBlkfK+i2gmDI/HENGjXA9uPhsUJ22p2OQFg3daaFx0/9qnWBRbOl9hHlvOw3OW/xs4Hf4rcnYzj+OeFOIHj4dtG7/2y+b3IhBGAqjUiQWQ9JI/ErDpop6gcei9z9ZIXHIhLaLSGRW8zYxIuaTZccxqsGfHDXvH4cf37Z4e3ihxVOTp5bf4E8N2u+3PWB2SP7tXsfsFl80rtOeZX/gvz6//7tmnFFzD2mkxnFgL710ToHH1eCcm/LU2aA9m027v+kBH8ipyHbACxAMWaV5I4v2ZgAzIxkUGXIqkn3xrhw4wVe8hoMmOwBmYJMiJy+lHPriNcSyrvgEgUS2h/vl1BcvSqgcZsPbbABrhgdgvhgvS6hIYsPP8MwTVR5SLZA4573xHMpCV7xGZBFmxyProfR64yNCgKh4hygjXIuvpdcbPyEayA2vsEpRHcgl6gtzr8A9ho0RlgQnBPoK4tV45gBfGQZ6KQBDqzRcjdeAqQwHUfYp+SohcQdc1/Ukm4Gw4dV6vqTkM+uQpRv8E2VPF/sPp9xSb2qlGH4AAAAASUVORK5CYII="


def base_64_img_decoder(b64: str) -> bytes:
    base64_img_bytes = b64.encode("utf-8")
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    return decoded_image_data


async def upload_to_s3_bucket(
    fileobj: str,
    folder: str,
    filename: str,
    extension: str,
):
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=s.ACCESS_KEY_ID,
        aws_secret_access_key=s.ACCESS_SECRET_KEY,
    )
    fileobj_b = base_64_img_decoder(fileobj)

    bucket = s3.Bucket(s.S3_IMAGES_BUCKET)
    s3_filename = f"{folder}{filename}{extension}"
    bucket.upload_fileobj(
        BytesIO(fileobj_b),
        s3_filename,
        ExtraArgs={"ContentType": "image/jpg"},
    )


async def get_presigned_url(
    session: AsyncSession,
    image_id: int,
    image_class: Type[PlaceImage | UserImage | CategoryImage],
) -> URL:
    image_data = (
        await session.execute(
            sa.select(
                image_class.s3_path,
                image_class.s3_filename,
                image_class.presigned_url,
                image_class.presigned_url_due,
            )
            .select_from(image_class)
            .where(
                image_class.id == image_id,
            )
        )
    ).fetchone()

    if (
        not image_data.presigned_url_due
        or image_data.presigned_url_due < datetime.datetime.now()
    ):
        presigned_url_due_date = datetime.datetime.now() + datetime.timedelta(seconds=s.S3_PRESIGNED_URL_EXPIRATION)
        presigned_url = create_presigned_url(
            f"{image_data.s3_path}{image_data.s3_filename}"
        )

        await session.execute(
            sa.update(image_class)
            .where(image_class.id == image_id)
            .values(
                {
                    image_class.presigned_url: presigned_url,
                    image_class.presigned_url_due: presigned_url_due_date,
                }
            )
        )
        return presigned_url
    return image_data.presigned_url


def create_presigned_url(fileobject: str) -> URL | None:
    """Generate a presigned URL to share an S3 object

    :param fileobject: string
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=s.ACCESS_KEY_ID,
        aws_secret_access_key=s.ACCESS_SECRET_KEY,
    )
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": s.S3_IMAGES_BUCKET, "Key": fileobject},
            ExpiresIn=s.S3_PRESIGNED_URL_EXPIRATION,
        )
    except ClientError as e:
        print(e)
        return None

    return response


async def add_imagetype_routine(
    extension: str,
    image__b64s: List[str],
    entity_id: str,
    session: AsyncSession,
    image_class: Type[PlaceImage | UserImage | CategoryImage],
) -> list[dict[str, URL | int]]:
    entity_id = decode_gql_id(entity_id)[1]
    uploaded_images = []
    for img in image__b64s:
        # TODO what if I get md5 of the whole picture and then put it here
        filename = encode_md5(f"UID{entity_id}{img[:16]}UID")
        if s.AWS_UPLOADING:
            await upload_to_s3_bucket(
                fileobj=img,
                folder=image_class.folder,
                filename=filename,
                extension=extension,
            )
        full_filename = f"{filename}{extension}"
        vals = {
            image_class.s3_path: image_class.folder,
            image_class.s3_filename: full_filename,
        }

        if image_class == PlaceImage:
            vals[image_class.place_id] = entity_id
        elif image_class == CategoryImage:
            vals[image_class.category_id] = entity_id
        elif image_class == UserImage:
            vals[image_class.user_id] = entity_id

        image_id: int = (
            (
                await session.execute(
                    sa.insert(image_class).values(vals).returning(image_class.id)
                )
            )
            .fetchone()
            .id
        )
        presigned_url = await get_presigned_url(
            session=session, image_id=image_id, image_class=image_class
        )

        image = {
            "id": image_id,
            "presigned_url": presigned_url if s.AWS_UPLOADING else "temp_string",
        }
        uploaded_images.append(image)
    return uploaded_images
