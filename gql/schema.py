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

    add_place = MutationAddPlace.Field()
    update_place = MutationUpdatePlace.Field()
    remove_place = MutationRemovePlace.Field()

    add_favourite_place = MutationAddFavouritePlace.Field()
    remove_favourite_place = MutationRemoveFavouritePlace.Field()

    add_follower = MutationAddFollower.Field()
    remove_follower = MutationRemoveFollower.Field()

    add_visited_place = MutationAddVisitedPlace.Field()
    # remove_visited_place = MutationRemoveVisitedPlace.Field(deprecation_reason="Unusable, might be deleted later")

    add_place_image = MutationAddPlaceImage.Field()
    add_user_image = MutationAddUserImage.Field()

    check_in_place = MutationCheckIn.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
