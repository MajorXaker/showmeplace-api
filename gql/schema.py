import graphene
from alchql.fields import FilterConnectionField

from gql.gql_types import (
    PlaceType,
    CategoryType,
    UserType,
    PlaceImageType,
    ActionType,
    EmailCheckAvailability,
    resolve_email_check_availability,
)
from gql.mutations import (
    MutationCheckIn,
    MutationRemoveFollower,
    MutationRemovePlace,
    MutationRemoveVisitedPlace,
    MutationOpenSecretPlace,
    MutationAddPlaceImage,
    MutationAddUserImage,
    MutationAddFollower,
    MutationUpdatePlace,
    MutationUpdateUser,
    MutationAddFavouritePlace,
    MutationRemoveFavouritePlace,
    MutationAddPlace,
    MutationCloseSecretPlace,
    MutationAddUser,
    MutationUpdateSecretPlaceData,
    MutationVerifyCognitoUser,
    MutationSigninSignupCognito,
    MutationForgotPassword,
)


class Query(graphene.ObjectType):
    select_places = FilterConnectionField(PlaceType)
    select_other_places = FilterConnectionField(
        PlaceType
    )  # TODO switch to fine queries
    select_users = FilterConnectionField(UserType)
    select_category = FilterConnectionField(CategoryType)
    select_place_images = FilterConnectionField(
        PlaceImageType, deprecation_reason="Won't be accessed directly"
    )
    select_actions = FilterConnectionField(ActionType)

    check_email_availability = graphene.NonNull(
        of_type=EmailCheckAvailability,
        email_address=graphene.Argument(type_=graphene.String, required=True),
        resolver=resolve_email_check_availability,
        deprecation_reason="Use mutation registration login",
    )


class Mutation(graphene.ObjectType):
    verify_cognito_user = MutationVerifyCognitoUser.Field(
        deprecation_reason="use registration login"
    )
    add_user = MutationAddUser.Field(deprecation_reason="use registrationLogin")
    update_user = MutationUpdateUser.Field()

    add_place = MutationAddPlace.Field()
    update_place = MutationUpdatePlace.Field()
    remove_place = MutationRemovePlace.Field()

    add_favourite_place = MutationAddFavouritePlace.Field()
    remove_favourite_place = MutationRemoveFavouritePlace.Field()

    add_follower = MutationAddFollower.Field()
    remove_follower = MutationRemoveFollower.Field()

    remove_visited_place = MutationRemoveVisitedPlace.Field(
        deprecation_reason="Service, will be deleted later"
    )

    add_place_image = MutationAddPlaceImage.Field()
    add_user_image = MutationAddUserImage.Field()

    check_in_place = MutationCheckIn.Field()

    open_secret_place = MutationOpenSecretPlace.Field()
    close_secret_place = MutationCloseSecretPlace.Field(
        deprecation_reason="Service, will be deleted later"
    )
    update_secret_place = MutationUpdateSecretPlaceData.Field()
    registration_login = MutationSigninSignupCognito.Field()

    forgot_password = MutationForgotPassword.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
