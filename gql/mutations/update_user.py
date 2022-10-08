import re

import boto3
import graphene
import sqlalchemy as sa
from graphql import GraphQLError
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_types.user_type import UserType
from models.db_models import User, EmailAddress
from models.enums import EmailStatusEnum
from utils.api_auth import AuthChecker
from utils.config import settings as s


class PasswordChange(graphene.InputObjectType):
    old_password = graphene.String()
    new_password = graphene.String()


class MutationUpdateUser(graphene.Mutation):
    class Meta:
        arguments = {
            # "name": graphene.String(), # we cannot change name as for now
            "description": graphene.String(),
            "new_email_address": graphene.String(),
            "passwords": graphene.Argument(PasswordChange),
        }
        output = UserType

    @classmethod
    async def mutate(cls, root, info, **values):
        # TODO address verification on change
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        cognito_connection = boto3.client(
            "cognito-idp",
            region_name="us-east-1",
            aws_access_key_id=s.ACCESS_KEY_ID,
            aws_secret_access_key=s.ACCESS_SECRET_KEY,
        )
        user = (
            await session.execute(sa.select(User.name).where(User.id == user_id))
        ).fetchone()

        if values.get("description"):
            await session.execute(
                sa.update(User)
                .where(User.id == user_id)
                .values({User.description: values.get("description")})
            )
        if values.get("new_email_address"):
            new_email_address = values["new_email_address"]
            is_not_available = (
                await session.execute(
                    sa.select(EmailAddress.id).where(
                        EmailAddress.address == new_email_address
                    )
                )
            ).fetchone()
            if is_not_available:
                raise ValueError("Email address is already in use")

            response = cognito_connection.admin_update_user_attributes(
                UserPoolId=s.COGNITO_USER_POOL,
                Username=user.name,
                UserAttributes=[
                    {"Name": "email", "Value": new_email_address},
                ],
            )

            old_email = (
                await session.execute(
                    sa.select(
                        EmailAddress.id, EmailAddress.status, EmailAddress.address
                    ).where(EmailAddress.user_id == user_id)
                )
            ).fetchone()

            if old_email.status not in ("BOUNCED", "COMPLAINED", "BLACKLISTED"):
                await session.execute(
                    sa.delete(EmailAddress).where(EmailAddress.id == old_email.id)
                )
            else:
                await session.execute(
                    sa.update(EmailAddress)
                    .where(EmailAddress.id == old_email.id)
                    .values({EmailAddress.user_id: None})
                )
            # TODO Routine for confirming email!!!!
            email_status = EmailStatusEnum.VERIFIED
            # TODO Routine for confirming email!!!!
            new_email = (
                await session.execute(
                    sa.insert(EmailAddress)
                    .values(
                        {
                            EmailAddress.address: new_email_address,
                            EmailAddress.user_id: user_id,
                            EmailAddress.status: email_status,
                        }
                    )
                    .returning(EmailAddress.id)
                )
            ).fetchone()

        if values.get("passwords"):
            new_password = values["passwords"].get("new_password")
            old_password = values["passwords"].get("old_password")
            if not new_password or not old_password:
                raise ValueError("Password cannot be empty")

            # TODO make use of old password

            # validators
            no_numbers = (
                "No numbers in password"
                if not re.findall(r"\d", new_password)
                else None
            )
            too_short = (
                "Password should at least of 6 symbols"
                if len(new_password) < 6
                else None
            )
            if no_numbers or too_short:
                errors = {}
                if no_numbers:
                    errors["No Numbers"] = no_numbers
                if too_short:
                    errors["Too Short"] = too_short
                message = ". ".join(errors.values())

                raise GraphQLError(
                    message,
                    extensions={
                        "type": "Value Error",
                        "exception_group": "Bad Password",
                        "reasons": tuple(errors.keys()),
                    },
                )

            response = cognito_connection.admin_set_user_password(
                UserPoolId=s.COGNITO_USER_POOL,
                Username=user.name,
                Password=new_password,
                Permanent=True,
            )

        return await UserType.get_node(info, user_id)
