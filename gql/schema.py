import graphene
from alchql.fields import FilterConnectionField

from gql.gql_types import CategoryType, PlaceImageType, PlaceType, UserType
from gql.mutations import (
    MutationRemoveFollower,
    MutationAddPlace,
    MutationAddUser,
    MutationCheckIn,
    MutationAddFavouritePlace,
    MutationAddFollower,
    MutationAddVisitedPlace,
    MutationRemoveFavouritePlace,
    MutationRemoveVisitedPlace,
    MutationUpdatePlace,
    MutationUpdateUser,
    MutationRemovePlace,
    MutationAddPlaceImage,
    MutationAddUserImage,
)


class Query(graphene.ObjectType):
    select_users = FilterConnectionField(UserType)
    select_places = FilterConnectionField(PlaceType)
    select_category = FilterConnectionField(CategoryType)
    select_place_images = FilterConnectionField(PlaceImageType)


class Mutation(graphene.ObjectType):
    add_user = MutationAddUser.Field()
    update_user = MutationUpdateUser.Field()

    # add_category = MutationAddCategory.Field(
    #     deprecation_reason="Service method. Do not use on production"
    # )
    # update_category = MutationUpdateCategory.Field(
    #     deprecation_reason="Service method. Do not use on production"
    # )
    # remove_category = MutationRemoveCategory.Field(
    #     deprecation_reason="Service method. Do not use on production"
    # )

    add_place = MutationAddPlace.Field()
    update_place = MutationUpdatePlace.Field()
    remove_place = MutationRemovePlace.Field()

    # update_coin_value = MutationUpdateCoinValue.Field()

    add_favourite_place = MutationAddFavouritePlace.Field()
    remove_favourite_place = MutationRemoveFavouritePlace.Field()

    add_follower = MutationAddFollower.Field()
    remove_follower = MutationRemoveFollower.Field()

    add_visited_place = MutationAddVisitedPlace.Field()
    remove_visited_place = MutationRemoveVisitedPlace.Field()

    add_place_image = MutationAddPlaceImage.Field()
    add_user_image = MutationAddUserImage.Field()
    # add_category_image = MutationAddCategoryImage.Field(
    #     deprecation_reason="Service method. Do not use on production"
    # )

    check_in_place = MutationCheckIn.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
