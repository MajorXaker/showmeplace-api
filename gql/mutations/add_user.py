import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import encode_gql_id
from models.db_models import User


class MutationAddUser(SQLAlchemyCreateMutation):
    class Meta:
        model = User

        # input_fields = {
        #     "price_kind": graphene.Enum.from_enum(PriceKind)(),
        #     "currency": graphene.Enum.from_enum(Currency)(),
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
                        User.coins: 0,
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
