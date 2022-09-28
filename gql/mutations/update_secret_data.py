from alchql import SQLAlchemyUpdateMutation

from gql.gql_types.place_type import PlaceType
from gql.gql_types.secret_place_extra_type import SecretPlaceExtraType
from models.db_models import Place, SecretPlaceExtra
from utils.api_auth import AuthChecker


class MutationUpdatePlace(SQLAlchemyUpdateMutation):
    class Meta:
        model = SecretPlaceExtra
        output = SecretPlaceExtraType
        input_type_name = "InputUpdatePlace"
        exclude_fields = [
            SecretPlaceExtra.place_id.key,
            SecretPlaceExtra.record_created.key,
            SecretPlaceExtra.record_modified.key
        ]

    @classmethod
    async def mutate(cls, root, info, value: dict, id):
        user_id = await AuthChecker.check_auth_mutation(
            session=info.context.session, info=info
        )
        result = await super().mutate(root, info, id, value)

        return result
