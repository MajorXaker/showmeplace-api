# import graphene
# from alchql import SQLAlchemyCreateMutation
# from graphene import String
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from models.db_models.images import PlaceImage
# from utils.api_auth import AuthChecker
# from utils.s3_object_tools import (
#     add_imagetype_routine,
# )
# from ..gql_id import decode_gql_id
#
#
# # TODO receive b64s as dict, it would allow utilisation of extensions and image ordering
# class MutationAddPlaceImage(SQLAlchemyCreateMutation):
#     class Meta:
#         model = PlaceImage
#         arguments = {
#             "place__id": graphene.ID(graphene.ID, required=True),
#             "image__b64s": graphene.List(graphene.String, required=True),
#         }
#
#     images__presigned__urls = graphene.List(of_type=String)
#
#     @classmethod
#     async def mutate(cls, root, info, place__id: str, image__b64s: list):
#         session: AsyncSession = info.context.session
#         user_id = await AuthChecker.check_auth_mutation(session=session, info=info)
#         file_extension = (
#             ".jpg"  # TODO implement a feature to load images of diffrent types
#         )
#         place__id = decode_gql_id(place__id)[1]
#         uploaded_images = await add_imagetype_routine(
#             extension=file_extension,
#             image__b64s=image__b64s,
#             entity_id=place__id,
#             session=session,
#             image_class=PlaceImage,  # WARNING might not work!
#         )
#         presigned_urls = [img["presigned_url"] for img in uploaded_images]
#         return MutationAddPlaceImage(images__presigned__urls=presigned_urls)
