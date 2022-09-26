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
    DELIVERED = "DELIVERED"
    VERIFIED = "VERIFIED"
    BOUNCED = "BOUNCED"
    BOUNCE_2ND_CHANCE = "BOUNCE_2ND_CHANCE"
    BOUNCE_3RD_CHANCE = "BOUNCE_3RD_CHANCE"
    COMPLAINED = "COMPLAINED"
    COMPLAIN_2ND_CHANCE = "COMPLAIN_2ND_CHANCE"
    BLACKLISTED = "BLACKLISTED"
