import graphene
from alchql import SQLAlchemyCreateMutation
from alchql.get_input_type import get_input_fields

from models.db_models import Category, Place
from models.db_models.place_image import PlaceImage
from ..gql_types.category_type import PlaceCategoryType
from ..gql_types.place_image_type import PlaceImageType

# TODO receive b64s as dict, it would allow utilisation of extensions and image ordering
class MutationAddPlaceImage(SQLAlchemyCreateMutation):
    class Meta:
        model = PlaceImage
        output = PlaceImageType
        arguments = {
            "place__id": graphene.ID(graphene.ID, required=True),
            "image__b64s": graphene.List(graphene.String, required=True),
        }

    @classmethod
    async def mutate(cls, root, info, place__id: str, image__b64s: list):
        # TODO Find out where you can fetch async session
        # create all necessary data - presigned url + its date + put file into s3
        # then create rows in place_image table with theese data

        return result
