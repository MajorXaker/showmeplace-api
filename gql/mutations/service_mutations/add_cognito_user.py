import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyCreateMutation
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import encode_gql_id
from models.db_models import User
from utils.config import settings as s


class MutationAddUser(SQLAlchemyCreateMutation):
    class Meta:
        model = User

        input_fields = {
            "email": graphene.String(),
            "password": graphene.String(),
        }

    just_added_to_base = graphene.Boolean()
    already_registered = graphene.Boolean()
    internal_id = graphene.String()

    @classmethod
    async def mutate(cls, root, info, value: dict):
        session: AsyncSession = info.context.session

        user_in_base = (
            await session.execute(
                sa.select(User.external_id, User.id).where(
                    User.external_id == value["external_id"]
                )
            )
        ).fetchone()
        if user_in_base:
            internal_id = encode_gql_id("UserType", user_in_base.id)
            return MutationAddUser(
                already_registered=True,
                just_added_to_base=False,
                internal_id=internal_id,
            )
        new_user_id = (
            await session.execute(
                sa.insert(User)
                .values(
                    {
                        User.name: value["name"],
                        User.external_id: value["external_id"],
                        User.external_id_type: value["external_id_type"],
                        User.coins: s.STARTING_COINS,
                        User.level: 0,
                    }
                )
                .returning(User.id)
            )
        ).fetchone()
        internal_id = encode_gql_id("UserType", new_user_id.id)

        return MutationAddUser(
            already_registered=False, just_added_to_base=True, internal_id=internal_id
        )
