# import api_models.models as m
import logging

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from utils.db import async_engine

# from core.db import get_session
# from utils.utils import get_decoded_gql_id

handle_email_complaint = APIRouter()


@handle_email_complaint.post("")
async def handle_complaint(req: Request):
    async with AsyncSession(async_engine) as session:
        pass
    logging.warning("GOT POST")
    body = await req.json()
    url = body["SubscribeURL"]
    logging.warning("URL")
    logging.warning(url)
    return "test-test"


@handle_email_complaint.post("")
async def handle_complaint(req: Request):
    logging.warning("Got get request")
    return "test-test"
