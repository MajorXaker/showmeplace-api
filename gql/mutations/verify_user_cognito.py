import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import encode_gql_id
from models.db_models import User, EmailAddress
from models.enums import EmailStatusEnum


# cognito_email_check = graphene.NonNull(
#     of_type=EmailCheckVerification,
#     email_address=graphene.Argument(type_=graphene.String, required=True),
#     external_id=graphene.Argument(type_=graphene.String, required=True),
#     resolver=resolve_email_check_verification
# )


class MutationVerifyCognitoUser(SQLAlchemyCreateMutation):
    class Meta:
        model = User
        input_fields = {
            "user_name": graphene.String(),
            "email_address": graphene.String(required=True),
            "external_id": graphene.String(required=True),
        }

    registered_now = graphene.Boolean()
    registered_earlier = graphene.Boolean()
    internal_id = graphene.String()

    @classmethod
    async def mutate(cls, root, info, value: dict):
        session: AsyncSession = info.context.session
        if False:
            # TODO section logic when email is incorrect
            raise ValueError("Incorrect email! Change email")

        user_in_base = (
            await session.execute(
                sa.select(User.external_id, User.id).where(
                    User.external_id == value["external_id"]
                )
            )
        ).fetchone()
        if user_in_base:
            internal_id = encode_gql_id("UserType", user_in_base.id)
            return MutationVerifyCognitoUser(
                registered_earlier=True,
                registered_now=False,
                internal_id=internal_id,
            )
        if not value["user_name"]:
            value["user_name"] = value["email_address"]
        new_user_id = (
            await session.execute(
                sa.insert(User)
                .values(
                    {
                        User.name: value["user_name"],
                        User.external_id: value["external_id"],
                        User.external_id_type: "COGNITO",
                        User.coins: 0,
                        User.level: 0,
                    }
                )
                .returning(User.id)
            )
        ).fetchone()
        internal_id = encode_gql_id("UserType", new_user_id.id)

        await session.execute(
            sa.insert(EmailAddress).values(
                {
                    EmailAddress.address: value["email_address"],
                    EmailAddress.user_id: new_user_id.id,
                    EmailAddress.status: EmailStatusEnum.VERIFIED,
                }
            )
        )

        return MutationVerifyCognitoUser(
            registered_earlier=False,
            registered_now=True,
            internal_id=internal_id,
        )
