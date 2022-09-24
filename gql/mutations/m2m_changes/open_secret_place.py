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


class MutationOpenSecretPlace(graphene.Mutation):
    class Meta:
        # model = M2MUserOpenedSecretPlace
        output = PlaceType
        arguments = {"open__place__id": graphene.ID(required=True)}

    @classmethod
    async def mutate(cls, root, info, open__place__id: str):
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
        place_id = decode_gql_id(open__place__id)[1]
        already_opened = (
            await session.execute(
                sa.select(M2MUserOpenedSecretPlace).where(
                    M2MUserOpenedSecretPlace.place_id == place_id,
                    M2MUserOpenedSecretPlace.user_id == user_id,
                )
            )
        ).fetchone()
        if already_opened:
            raise ValueError("Place already opened")
        opening_possible = (
            await ActionsEconomy.verify_possibility(
                session=session, user_id=user_id, action_names=["Open a secret place"]
            )
        )["Open a secret place"]
        if opening_possible:

            owner = (
                await session.execute(
                    sa.select(Place.owner_id.label("id")).where(Place.id == place_id)
                )
            ).fetchone()

            await session.execute(
                sa.insert(M2MUserOpenedSecretPlace).values(
                    {
                        M2MUserOpenedSecretPlace.place_id: place_id,
                        M2MUserOpenedSecretPlace.user_id: user_id,
                    }
                )
            )
            await ActionsEconomy.execute(
                session=session,
                action_name="Open a secret place",
                coin_receiver_user_id=user_id,
            )
            await ActionsEconomy.execute(
                session=session,
                action_name="Have your secret place opened",
                coin_receiver_user_id=owner.id,
            )
        else:
            raise ActionsEconomy.InsufficientCoins("Not enough coins to open")

        return await PlaceType.get_node(info, place_id)
