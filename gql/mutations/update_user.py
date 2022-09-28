import graphene
from alchql import SQLAlchemyUpdateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from gql.gql_id import decode_gql_id
from gql.gql_types.user_type import UserType
from models.db_models import User, EmailAddress
from models.enums import EmailStatusEnum
from utils.api_auth import AuthChecker


class MutationUpdateUser(SQLAlchemyUpdateMutation):
    class Meta:
        model = User
        input_fields = get_input_fields(
            model=User,
            exclude_fields=[
                User.coins.key,
                User.record_created.key,
                User.record_modified.key,
                User.id.key,
                User.external_id.key,
                User.external_id_type.key,
            ],
        ) | {"new_email_address": graphene.String()}
        # get_input_fields(
        #     model=EmailAddress,
        #     only_fields=[EmailAddress.address.key]
        # )

        output = UserType
        input_type_name = "InputUpdateUser"

    @classmethod
    async def mutate(cls, root, info, id, value: dict):
        # TODO address verification on change
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        user_to_upd = decode_gql_id(info.variable_values["updateUserId"])[1]
        new_email_address = value.pop("new_email_address")
        await session.execute(
            sa.update(EmailAddress)
            .where(
                sa.and_(
                    EmailAddress.user_id == user_to_upd,
                    EmailAddress.status == EmailStatusEnum.VERIFIED,
                )
            )
            .values({EmailAddress.address: new_email_address})
        )
        result = await super().mutate(root, info, id, value)

        return result
