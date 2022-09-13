import graphene
from alchql import SQLAlchemyDeleteMutation

from gql.gql_types.place_type import PlaceType
from models.db_models import Place


class MutationRemovePlace(SQLAlchemyDeleteMutation):
    class Meta:
        model = Place
        output = PlaceType
        input_type_name = "InputUpdatePlace"

    is_success = graphene.Boolean()
