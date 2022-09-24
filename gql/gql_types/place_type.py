import graphene
from alchql import SQLAlchemyObjectType
from alchql.batching import get_batch_resolver
from alchql.fields import ModelField
from alchql.node import AsyncNode
from alchql.utils import FilterItem
from graphene import ObjectType, String, Int

from models.db_models import Place, Category
from models.enums import SecretPlacesFilterEnum, DecayingPlacesFilterEnum
from utils.filters import secrets_filter, decaying_filter


class DistanceFilterInput(ObjectType):
    longitude_from = graphene.Float(required=True)
    latitude_from = graphene.Float(required=True)
    distance_from = graphene.Int(required=True)

class PlaceType(SQLAlchemyObjectType):
    class Meta:
        model = Place
        interfaces = (AsyncNode,)
        filter_fields = {
            "secrets_filter": FilterItem(
                field_type=graphene.Enum.from_enum(SecretPlacesFilterEnum),
                filter_func=secrets_filter,
            ),
            "decay_filter": FilterItem(
                field_type=graphene.Enum.from_enum(DecayingPlacesFilterEnum),
                filter_func=decaying_filter,
            ),
            "distance_filter": FilterItem(
                field_type=graphene.ObjectType(of_type),
                filter_func=None
            )
        }

    # image = ModelField(
    #     V2CategoryType,
    #     model_field=Category,
    #     resolver=get_batch_resolver(m.Description.image.property, single=True),
    #     use_label=False,
    #     deprecation_reason="Use lot.description",
    # )


    # id = external(graphene.ID(required=True))
    #
    # def resolve_id(self, info):
    #     return encode_gql_id(self.__class__.__name__, self.id)
