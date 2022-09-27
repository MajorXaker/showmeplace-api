# import api_models.models as m
from fastapi import APIRouter
from starlette.requests import Request

# from core.db import get_session
# from utils.utils import get_decoded_gql_id

handle_email_bounce = APIRouter()


@handle_email_bounce.post("")
async def handle_bounce(req: Request):
    asdfadfgf = 5 + 5
    aaa = 5

    body = await req.json()
    print(body["SubscribeURL"])
    return aaa
