from alchql import SQLAlchemyUpdateMutation

from gql.gql_types.place_type import PlaceType
from models.db_models import Place
from utils.api_auth import AuthChecker


class MutationUpdatePlace(SQLAlchemyUpdateMutation):
    class Meta:
        model = Place
        output = PlaceType
        input_type_name = "InputUpdatePlace"
        only_fields = [
            Place.name.key,
            Place.description.key
        ]

    @classmethod
    async def mutate(cls, root, info, value: dict, id):
        user_id = await AuthChecker.check_auth_mutation(
            session=info.context.session, info=info
        )
        result = await super().mutate(root, info, id, value)

        return result
