import json
import logging

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

# import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert
from models.db_models import EmailAddress
from models.enums import EmailStatusEnum
from utils.db import async_engine


handle_email_complaint = APIRouter()

# /handle-email-complaint
@handle_email_complaint.post("")
async def handle_bounce(req: Request):
    async with AsyncSession(async_engine) as session:
        logging.warning("GOT POST")
        body = await req.json()
        confirmation_url = body.get("SubscribeURL")
        if confirmation_url:
            logging.warning("URL")
            logging.warning(confirmation_url)
            return
        if body.get("Type") == "Notification":
            msg = body.get("Message")
            if not msg:
                return
            msg = json.loads(body["Message"])
            if msg.get("complaint"):
                for address in msg["complaint"]["complainedRecipients"]:
                    await session.execute(
                        pg_insert(EmailAddress)
                        .values(
                            {
                                EmailAddress.address: address["emailAddress"],
                                EmailAddress.status: EmailStatusEnum.COMPLAINED,
                            }
                        )
                        .on_conflict_do_nothing(index_elements=["address"])
                    )
        await session.commit()
    logging.info("Add new adress to db with Complaioned status")
    return "Success"

@handle_email_complaint.post("")
async def handle_complaint(req: Request):
    logging.warning("Got get request")
    return "test-test"
