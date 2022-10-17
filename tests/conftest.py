import asyncio
from contextlib import asynccontextmanager
from inspect import isawaitable
from typing import Any
from unittest.mock import patch

import pytest
from alchql.app import SessionQLApp
from alchql.gql_id import ResolvedGlobalId
from alchql.middlewares import LoaderMiddleware
from fastapi import FastAPI
# from fastjwk import JWKBearer, JWTAuthorizationCredentials
# from api_models.models import Model
from graphene import Context
from graphql import ASTValidationRule, GraphQLError
from httpx import AsyncClient
# from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from starlette.background import BackgroundTasks
from starlette.requests import HTTPConnection

from models.base_engine import Model
from utils.config import settings as st
# from config import settings as st
# from core.db import get_session
# from gql.middlewares import AuthMiddleware, StytchAuthMiddleware
from gql.schema import schema
from tests.creator import Creator
from utils.db import get_session

db_url = (
    "postgresql+asyncpg://"
    f"{st.DATABASE_USER}:"
    f"{st.DATABASE_PASSWORD}@"
    f"{st.DATABASE_HOST}:"
    f"{st.DATABASE_PORT}/"
    f"{st.DATABASE_DB}"
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def check_test_db():
    if (
        st.DATABASE_HOST not in ("localhost", "127.0.0.1", "postgres")
        or "amazonaws" in st.DATABASE_HOST
    ):
        print(db_url)
        raise Exception("Use local database only!")


@pytest.fixture(scope="session")
async def engine():
    check_test_db()

    e = create_async_engine(db_url, echo=False, max_overflow=25)

    try:
        async with e.begin() as con:
            await con.run_sync(Model.metadata.create_all)

        yield e
    finally:
        async with e.begin() as con:
            await con.run_sync(Model.metadata.drop_all)


@pytest.fixture
async def dbsession(engine) -> AsyncSession:
    async with AsyncSession(bind=engine) as session:
        yield session


def get_test_app(session: AsyncSession):
    class _SessionQLApp(SessionQLApp):
        def __init__(self, *args, **kwargs):
            super().__init__(engine=None, *args, **kwargs)

        @asynccontextmanager
        async def _get_context_value(self, request: HTTPConnection) -> Any:
            if callable(self.context_value):
                context = self.context_value(
                    request=request,
                    background=BackgroundTasks(),
                    session=session,
                )
                if isawaitable(context):
                    context = await context
                yield context
            else:
                yield self.context_value or {
                    "request": request,
                    "background": BackgroundTasks(),
                    "session": session,
                }

    app = FastAPI()
    app.add_route(
        "/graphql",
        _SessionQLApp(
            schema=schema,
            middleware=[
                LoaderMiddleware(Model.registry.mappers),
                # AuthMiddleware(),
                # StytchAuthMiddleware(),
            ],
            context_value=Context,
        ),
    )
    return app


@pytest.fixture
def test_client_rest(dbsession) -> FastAPI:
    from main import app

    def override_get_db():
        test_db = dbsession
        yield test_db

    app.dependency_overrides[get_session] = override_get_db

    yield app


@pytest.fixture
async def test_client_graph(dbsession) -> AsyncClient:
    test_app = get_test_app(dbsession)
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


# @pytest.fixture
# def patch_jwk(mocker: MockerFixture):
#     def fun(sub):
#         async def call(self, request):
#             return JWTAuthorizationCredentials(
#                 jwt_token="",
#                 header="",
#                 claims={"sub": sub, "roles": []},
#                 signature="",
#                 message="",
#             )
#
#         return mocker.patch.object(JWKBearer, "__call__", call)
#
#     return fun


# @pytest.fixture
# def patch_auth(mocker: MockerFixture, patch_jwk):
#     def inner(authenticated=False, external_id="cognito_user_id"):
#         patch_jwk(external_id)
#         mocker.patch.object(
#             AuthMiddleware,
#             "process_auth",
#             return_value={
#                 "id": ResolvedGlobalId("UserType", 1).encode(),
#                 "externalId": external_id,
#                 "email": "a@a.com",
#             }
#             if authenticated
#             else None,
#         )
#
#     return inner


@pytest.fixture
def raise_graphql():
    def report_error(self, x, *args, **kwargs):
        raise x

    def gql_error_init(
        self,
        message: str,
        nodes=None,
        source=None,
        positions=None,
        path=None,
        original_error=None,
        extensions=None,
    ):
        raise original_error or Exception(message)

    with patch.object(ASTValidationRule, "report_error", report_error), patch.object(
        GraphQLError, "__init__", gql_error_init
    ):
        yield


@pytest.fixture
def creator(dbsession) -> Creator:
    return Creator(dbsession)
