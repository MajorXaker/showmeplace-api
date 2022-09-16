from utils.enums_base import StrEnum


class CoinChange(StrEnum):
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

