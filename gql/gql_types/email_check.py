import boto3
import graphene
import sqlalchemy as sa
from graphene import Boolean
from utils.config import settings as s
from models.db_models import EmailAddress, User


class EmailCheckAvailability(graphene.ObjectType):
    is_available = graphene.Boolean()


async def resolve_email_check_availability(query, info, email_address):
    session = info.context.session
    is_in_list = (
        await session.execute(
            sa.select(EmailAddress).where(EmailAddress.address == email_address)
        )
    ).fetchone()
    # return "True" if is_in_list else "False"
    return EmailCheckAvailability(is_available=False if is_in_list else True)
