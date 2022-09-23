import graphene
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import decode_gql_id
from models.db_models.m2m.m2m_user_place_favourite import M2MUserPlaceFavourite
from utils.api_auth import AuthChecker


class MutationRemoveFavouritePlace(graphene.Mutation):
    class Meta:
        model = M2MUserPlaceFavourite
        arguments = {
            "place_id": graphene.String(required=True),
        }

    is_success = graphene.Boolean()

    @classmethod
    async def mutate(cls, root, info, place_id: str):
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        place_id = decode_gql_id(place_id)[1]

        await session.execute(
            sa.delete(M2MUserPlaceFavourite).where(
                sa.and_(
                    M2MUserPlaceFavourite.user_id == user_id,
                    M2MUserPlaceFavourite.place_id == place_id,
                )
            )
        )

        return MutationRemoveFavouritePlace(is_success=True)
