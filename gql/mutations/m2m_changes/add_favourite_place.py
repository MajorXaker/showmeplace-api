from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import decode_gql_id
from gql.gql_types.place_type import PlaceType
from models.db_models.m2m.m2m_user_place_favourite import M2MUserPlaceFavourite
from utils.api_auth import AuthChecker


class MutationAddFavouritePlace(SQLAlchemyCreateMutation):
    class Meta:
        model = M2MUserPlaceFavourite
        output = PlaceType
        input_fields = get_input_fields(
            model=M2MUserPlaceFavourite,
            only_fields=[
                M2MUserPlaceFavourite.place_id.key,
            ],
            required_fields=[
                M2MUserPlaceFavourite.place_id.key,
            ],
        )

    @classmethod
    async def mutate(cls, root, info, value: dict):
        session: AsyncSession = info.context.session
        user_id = await AuthChecker.check_auth_mutation(session=session, info=info)

        value["place_id"] = decode_gql_id(value["place_id"])[1]
        value["user_id"] = user_id
        result = await super().mutate(root, info, value)

        return result