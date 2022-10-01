import json
import logging

from fastapi import APIRouter
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from models.db_models import EmailAddress
from models.enums import EmailStatusEnum
from utils.db import async_engine

handle_email_bounce = APIRouter()

# /handle-email-complaint
@handle_email_bounce.post("")
async def handle_complaint(req: Request):
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
            if msg.get("bounce"):
                for address in msg["bounce"]["bouncedRecipients"]:
                    await session.execute(
                        pg_insert(EmailAddress)
                        .values(
                            {
                                EmailAddress.address: address["emailAddress"],
                                EmailAddress.status: EmailStatusEnum.BOUNCED,
                            }
                        )
                        .on_conflict_do_nothing(index_elements=["address"])
                    )
        await session.commit()
    logging.info("Add new adress to db with BOUNCED status")
    return "Success"


@handle_email_bounce.post("")
async def handle_complaint(req: Request):
    logging.warning("Got get request")
    return "test-test"
