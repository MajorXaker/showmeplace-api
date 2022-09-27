# import api_models.models as m
import logging

from fastapi import APIRouter
from starlette.requests import Request

# from core.db import get_session
# from utils.utils import get_decoded_gql_id

handle_email_bounce = APIRouter()


@handle_email_bounce.post("")
async def handle_bounce(req: Request):
    body = await req.json()
    url = body["SubscribeURL"]
    logging.warning("URL")
    logging.warning(url)
    return "test-test"


@handle_email_bounce.post("")
async def handle_complaint(req: Request):
    logging.warning("Got get request")
    return "test-test"
