from utils.enums_base import StrEnum


class CoinChangeEnum(StrEnum):
    INCREASE = "INCREASE"
    DECREASE = "DECREASE"


class EntityImage(StrEnum):
    CATEGORY = "CATEGORY"
    USER = "USER"
    PLACE = "PLACE"


class IdentificationEnum(StrEnum):
    COGNITO = "COGNITO"
    META = "META"


class CoinValueChangeEnum(StrEnum):
    SPEND = "SPEND"
    EARN = "EARN"


class SecretPlacesFilterEnum(StrEnum):
    ALL = "ALL"
    SECRET = "SECRET"
    REGULAR = "REGULAR"


class DecayingPlacesFilterEnum(StrEnum):
    ALL = "ALL"
    DECAYED = "DECAYED"
    DECAYING = "DECAYING"
    REGULAR = "REGULAR"


class EmailStatusEnum(StrEnum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    BOUNCED = "BOUNCED"
    COMPLAINED = "COMPLAINED"
    BLACKLISTED = "BLACKLISTED"
    # these 3 are debatable and may be redundant
    BOUNCE_2ND_CHANCE = "BOUNCE_2ND_CHANCE"
    BOUNCE_3RD_CHANCE = "BOUNCE_3RD_CHANCE"
    COMPLAIN_2ND_CHANCE = "COMPLAIN_2ND_CHANCE"
