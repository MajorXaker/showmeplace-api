import graphene
from alchql.fields import FilterConnectionField

from gql.gql_types.category_type import PlaceCategoryType
from gql.gql_types.place_type import PlaceType
from gql.gql_types.user_type import UserType
from gql.mutations import (
    MutationRemoveFollower,
    MutationAddPlace,
    MutationAddUser,
    MutationUpdateCoinValue,
    MutationAddFavouritePlace,
    MutationAddFollower,
    MutationAddVisitedPlace,
    MutationRemoveFavouritePlace,
    MutationRemoveVisitedPlace,
    MutationUpdatePlace,
    MutationUpdateUser,
    MutationAddCategory,
    MutationUpdateCategory,
    MutationRemoveCategory,
    MutationRemovePlace,
)


class Query(graphene.ObjectType):
    select_users = FilterConnectionField(UserType)
    select_places = FilterConnectionField(PlaceType)
    select_category = FilterConnectionField(PlaceCategoryType)


class Mutation(graphene.ObjectType):
    add_user = MutationAddUser.Field()
    update_user = MutationUpdateUser.Field()

    add_category = MutationAddCategory.Field()
    update_category = MutationUpdateCategory.Field()
    remove_category = MutationRemoveCategory.Field()

    add_place = MutationAddPlace.Field()
    update_place = MutationUpdatePlace.Field()
    remove_place = MutationRemovePlace.Field()

    update_coin_value = MutationUpdateCoinValue.Field()

    add_favourite_place = MutationAddFavouritePlace.Field()
    remove_favourite_place = MutationRemoveFavouritePlace.Field()

    add_follower = MutationAddFollower.Field()
    remove_follower = MutationRemoveFollower.Field()

    add_visited_place = MutationAddVisitedPlace.Field()
    remove_visited_place = MutationRemoveVisitedPlace.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
