# import api_models.models as m
import sqlalchemy as sa
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from utils.config import settings as s
from facepy import SignedRequest
from utils.db import get_session

# from core.db import get_session
# from utils.utils import get_decoded_gql_id

delete_user_meta = APIRouter()


def parse_signed_request(signed_request):
    FB_APP_SECRET = s.META_APP_SECRET
    signed_data = SignedRequest.parse(signed_request, FB_APP_SECRET)
    return signed_data


async def delete_facebook_data(request, data):
    try:
        signed_request = request.POST["signed_request"]
        signed_data = parse_signed_request(signed_request)

        # Do User Data Deletion here

        # user_obj = User.objects.filter(id=signed_data["user_id"])
        # user_obj.delete()
        confirmation_code = 200
    except Exception as e:
        confirmation_code = 403
    return {
        "url": f"{s.APP_URL}/user_deletion_status/{confirmation_code}",
        "confirmation_code": confirmation_code,
    }


@delete_user_meta.get("")
async def delete_user_data_meta(req: Request):

    aaa = 5
    # decoded_gql_id = decode_gql_id(lot_id)
    # q = await db.execute(
    #     sa.select(m.Artwork.uid)
    #     .select_from(
    #         sa.join(
    #             m.Lot,
    #             m.Artwork,
    #             m.Lot.artwork_id == m.Artwork.id,
    #         )
    #     )
    #     .where(m.Lot.raw_lot_id == decoded_gql_id)
    # )
    # artwork_uid = q.scalar()

    return True


@delete_user_meta.post("")
async def delete_user_data_meta(req: Request):

    aaa = 5
    # decoded_gql_id = decode_gql_id(lot_id)
    # q = await db.execute(
    #     sa.select(m.Artwork.uid)
    #     .select_from(
    #         sa.join(
    #             m.Lot,
    #             m.Artwork,
    #             m.Lot.artwork_id == m.Artwork.id,
    #         )
    #     )
    #     .where(m.Lot.raw_lot_id == decoded_gql_id)
    # )
    # artwork_uid = q.scalar()

    return True
