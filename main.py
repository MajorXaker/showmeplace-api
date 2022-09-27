import logging

import sqlalchemy as sa
import uvicorn
from alchql.app import SessionQLApp
from alchql.middlewares import LogMiddleware
from fastapi import FastAPI

from gql.schema import schema
from utils.db import async_engine
from utils.config import settings as s
from utils.sns_webhooks.email_bounce import handle_email_bounce
from utils.sns_webhooks.email_complaint import handle_email_complaint

app = FastAPI()

middleware = [
    LogMiddleware(),
]


@app.on_event("startup")
async def connect_database_engine() -> None:
    async with async_engine.connect() as conn:
        await conn.scalar(sa.select(1))


app.add_route(
    "/graphql",
    SessionQLApp(
        schema=schema,
        middleware=middleware,
        # extensions=extensions,
        engine=async_engine,
    ),
)

app.include_router(
    handle_email_bounce,
    prefix="/handle-email-bounce",
)
app.include_router(
    handle_email_complaint,
    prefix="/handle-email-complaint",
)

if __name__ == "__main__":
    print("starting")
    logging.warning("Test")
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=s.SERVER_RELOAD_MODE,
        log_config=None,
    )
