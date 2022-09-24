from alchql import SQLAlchemyUpdateMutation

from gql.gql_types.place_type import PlaceType
from models.db_models import Place
from utils.api_auth import AuthChecker


class MutationUpdatePlace(SQLAlchemyUpdateMutation):
    class Meta:
        model = Place
        output = PlaceType
        input_type_name = "InputUpdatePlace"
        exclude_fields = [
            Place.record_created.key,
            Place.record_modified.key,
            Place.coordinate_longitude.key,
            Place.coordinate_latitude.key,
            Place.category_id.key,
            Place.owner_id.key,
            Place.address.key,
            Place.is_secret_place.key
        ]

    @classmethod
    async def mutate(cls, root, info,  value: dict, id):
        user_id = await AuthChecker.check_auth_mutation(
            session=info.context.session, info=info
        )
        result = await super().mutate(root, info, id, value)

        return result
