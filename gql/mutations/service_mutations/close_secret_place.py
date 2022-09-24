import graphene
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from gql.gql_id import decode_gql_id
from gql.gql_types import PlaceType
from gql.gql_types.user_type import UserType
from models.db_models import M2MUserOpenedSecretPlace, Place, ActionsEconomy
from models.db_models.m2m.m2m_user_user_following import M2MUserFollowingUser
from utils.api_auth import AuthChecker


class MutationCloseSecretPlace(graphene.Mutation):
    class Meta:
        # model = M2MUserOpenedSecretPlace
        # output = PlaceType
        arguments = {"open__place__id": graphene.ID(required=True)}

    is_success = graphene.Boolean()

    @classmethod
    async def mutate(cls, root, info, open__place__id: str):
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        place_id = decode_gql_id(open__place__id)[1]

        # try:
        await session.execute(
            sa.delete(M2MUserOpenedSecretPlace).where(
                M2MUserOpenedSecretPlace.place_id == place_id,
                M2MUserOpenedSecretPlace.user_id == user_id,
            )
        )
        # except:
        #     pass

        return MutationCloseSecretPlace(is_success=True)
