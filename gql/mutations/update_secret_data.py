from alchql import SQLAlchemyUpdateMutation
from alchql.get_input_type import get_input_fields

from gql.gql_types.place_type import PlaceType
from gql.gql_types.secret_place_extra_type import SecretPlaceExtraType
from models.db_models import Place, SecretPlaceExtra
from utils.api_auth import AuthChecker


class MutationUpdateSecretPlaceData(SQLAlchemyUpdateMutation):
    class Meta:
        model = SecretPlaceExtra
        output = SecretPlaceExtraType
        input_type_name = "InputUpdateSecretPlaceData"
        input_fields = get_input_fields(
            model=SecretPlaceExtra,
            exclude_fields=[
                SecretPlaceExtra.id.key,
                SecretPlaceExtra.record_created.key,
                SecretPlaceExtra.record_modified.key
            ],
        )
        exclude_fields = [
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
