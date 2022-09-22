import sqlalchemy as sa
import uvicorn
from alchql.app import SessionQLApp
from alchql.middlewares import LogMiddleware
from fastapi import FastAPI

from gql.schema import schema
from utils.config import settings as s
from utils.data_deletion.check_is_data_used import check_userdata
from utils.data_deletion.meta_deletion import delete_user_data_meta, delete_user_meta

# from utils.data_deletion.meta_deletion import get_artwork_uid_by_lot_id_router
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
app.include_router(
    delete_user_meta,
    prefix="/user-data-deletion-meta",
)
app.include_router(
    check_userdata,
    prefix="/is-my-data-in-showmeplace",
)
# app.add_route(
#     "/is-my-data-in-showmeplace",
#     check_userdata_in_showmeplace,
# )


app.add_route(
    "/delete-user-data",
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
        reload=s.SERVER_RELOAD_MODE,
        log_config=None,
    )
