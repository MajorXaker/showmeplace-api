import sqlalchemy as sa
import uvicorn
from alchql.app import SessionQLApp
from fastapi import FastAPI

from gql.schema import schema
from utils.db import engine

app = FastAPI()



@app.on_event("startup")
async def connect_database_engine() -> None:
    async with engine.connect() as conn:
        await conn.scalar(sa.select(1))


app.add_route(
    "/graphql",
    SessionQLApp(
        schema=schema,
        # middleware=middleware,
        # extensions=extensions,
        engine=engine,
    ),
)

if __name__ == "__main__":
    print("starting")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=False,
        log_config=None,
    )
