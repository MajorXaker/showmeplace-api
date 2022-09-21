import graphene
from alchql import SQLAlchemyDeleteMutation

from gql.gql_types.place_type import PlaceType
from models.db_models import Place
from utils.api_auth import AuthChecker


class MutationRemovePlace(SQLAlchemyDeleteMutation):
    class Meta:
        model = Place
        output = PlaceType
        input_type_name = "InputUpdatePlace"

    is_success = graphene.Boolean()

    @classmethod
    async def mutate(cls, root, info, value: dict):
        user_id = AuthChecker.check_auth_mutation(
            session=info.context.session, info=info
        )
        result = await super().mutate(root, info, value)

        return result
