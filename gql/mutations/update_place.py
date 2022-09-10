from alchql import SQLAlchemyUpdateMutation

from gql.gql_types.place_type import PlaceType
from models.db_models import Place


class MutationUpdatePlace(SQLAlchemyUpdateMutation):
    class Meta:
        model = Place
        output = PlaceType
        input_type_name = "InputUpdatePlace"
