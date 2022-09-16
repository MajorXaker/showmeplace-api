import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models import User


class MutationAddUser(SQLAlchemyCreateMutation):
    class Meta:
        model = User
        input_fields = get_input_fields(
            model=User,
            exclude_fields=[
                User.id.key,
                User.level.key,
                User.coins.key,
                User.record_created.key,
                User.record_modified.key,
            ],
            required_fields=[
                User.name.key,
                User.external_id.key,
                User.external_id_type.key,
            ],
        )
        input_type_name = "InputAddUser"

    just_added_to_base = graphene.Boolean()
    already_registered = graphene.Boolean()

    @classmethod
    async def mutate(cls, root, info, value: dict):
        session: AsyncSession = info.context.session

        user_in_base = (
            await session.execute(
                sa.select(User.external_id).where(User.external_id == value["external_id"])
            )
        ).fetchone()
        if user_in_base:
            return MutationAddUser(already_registered=True, just_added_to_base=False)
        await session.execute(
            sa.insert(User).values(
                {
                    User.name: value["name"],
                    User.external_id: value["external_id"],
                    User.external_id_type: value["external_id_type"],
                }
            )
        )

        return MutationAddUser(already_registered=False, just_added_to_base=True)
