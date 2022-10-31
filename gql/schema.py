import graphene
from alchql.fields import FilterConnectionField

from gql.gql_types import (
    PlaceType,
    CategoryType,
    UserType,
    PlaceImageType,
    ActionType,
    # SecretPlaceExtraType,
    ActionType,
    OldPlaceType,
    ActionType,
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
    select_users = FilterConnectionField(UserType)
    select_places = FilterConnectionField(PlaceType)
    select_category = FilterConnectionField(CategoryType)
    select_place_images = FilterConnectionField(
        PlaceImageType, deprecation_reason="Won't be accessed directly"
    )
    select_actions = FilterConnectionField(ActionType)

    old_select_places = FilterConnectionField(OldPlaceType, deprecation_reason="OLD")

    # check_email_availability = graphene.NonNull(
    #     of_type=EmailCheckAvailability,
    #     email_address=graphene.Argument(type_=graphene.String, required=True),
    #     resolver=resolve_email_check_availability,
    # )
    # cognito_email_check = graphene.NonNull(
    #     of_type=EmailCheckVerification,
    #     email_address=graphene.Argument(type_=graphene.String, required=True),
    #     external_id=graphene.Argument(type_=graphene.String, required=True),
    #     resolver=resolve_email_check_verification
    # )


class Mutation(graphene.ObjectType):
    verify_cognito_user= MutationVerifyCognitoUser.Field()
    add_user = MutationAddUser.Field()
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
    # registration_login = MutationRegistrationLoginCognito.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
