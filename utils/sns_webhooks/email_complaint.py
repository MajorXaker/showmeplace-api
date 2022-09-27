# import api_models.models as m
import logging

from fastapi import APIRouter
from starlette.requests import Request

# from core.db import get_session
# from utils.utils import get_decoded_gql_id

handle_email_complaint = APIRouter()


@handle_email_complaint.post("")
async def handle_complaint(req: Request):
    body = await req.json()
    url = body["SubscribeURL"]
    logging.warning("URL")
    logging.warning(url)
    return "test-test"
