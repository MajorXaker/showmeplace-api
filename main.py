import sqlalchemy as sa
import uvicorn
from alchql.app import SessionQLApp
from alchql.middlewares import LogMiddleware
from fastapi import FastAPI

from gql.schema import schema
from utils.db import async_engine

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

if __name__ == "__main__":
    print("starting")
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
        log_config=None,
    )
