from .m2m_changes import *
from .service import (
    MutationCloseSecretPlace,
    MutationRemoveVisitedPlace,
)

from .add_user import MutationAddUser
from .update_user import MutationUpdateUser
from .add_place import MutationAddPlace
from .update_place import MutationUpdatePlace
from gql.mutations.remove_place import MutationRemovePlace
from .add_place_image import MutationAddPlaceImage
from .add_user_image import MutationAddUserImage
from .mutation_check_in import MutationCheckIn
from .update_secret_data import MutationUpdateSecretPlaceData
from .verify_user_cognito import MutationVerifyCognitoUser
from .signin_signup_cognito import MutationSigninSignupCognito
from .forgot_password import MutationForgotPassword
