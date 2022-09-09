# from alchql import SQLAlchemyCreateMutation
# from alchql.get_input_type import get_input_fields
#
# from models.db_models import User, M2MUserPlaceFavourite, Place
# from ..gql_types.place_type import PlaceType
# from ..gql_types.user_type import UserType
#
#
# class MutationAddFavouritePlace(SQLAlchemyCreateMutation):
#     class Meta:
#         model = M2MUserPlaceFavourite
#         output = PlaceType
#         input_fields = get_input_fields(
#             model=User,
#             only_fields=[User.id.key],
#             required_fields=[User.id.key],
#         ) | get_input_fields(
#             model=Place,
#             only_fields=[Place.id.key],
#             required_fields=[Place.id.key],
#         )
#
#     # @classmethod
#     # async def mutate(cls, root, info, value: dict):
#     #
#     #     result = await super().mutate(root, info, value)
#     #
#     #
#     #     return result
