# import api_models.models as m
import asyncio

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models import EmailAddress
from models.enums import EmailStatusEnum
from utils.db import async_engine


# from core.db import get_session
# from utils.utils import get_decoded_gql_id


async def body():
    async with AsyncSession(async_engine) as session:
        await session.execute(
            sa.insert(EmailAddress).values(
                {
                    EmailAddress.address: "bounce@simulator.amazonses.com",
                    EmailAddress.status: EmailStatusEnum.BOUNCED,
                }
            )
        )
        aaa = 5


if __name__ == "__main__":
    asyncio.run(body)
