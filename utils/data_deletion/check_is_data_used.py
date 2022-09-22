# import api_models.models as m
import sqlalchemy as sa
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.applications import Starlette
from starlette.requests import Request

from gql.gql_id import decode_gql_id
from models.db_models import User
from utils.db import get_session, async_engine

# from core.db import get_session
# from utils.utils import get_decoded_gql_id

check_userdata = APIRouter()


@check_userdata.get("")
async def check_userdata_in_showmeplace(req: Request):
    async with AsyncSession(async_engine) as session:
        external_id = req.query_params.get("user")
        if not external_id:
            return "No results. No id provided"
        user = (await session.execute(
            sa.select(User.external_id)
            .where(User.external_id == external_id)
        )).fetchone()
        if user:
            return "User exists in ShowMePlace database"
        else:
            return "User does not exists in ShowMePlace database"