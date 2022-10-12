from typing import Tuple

from graphql import GraphQLError

from utils.enums_base import StrEnum


class ExceptionGroupEnum(StrEnum):
    EMAIL = "Bad Email"
    PASSWORD = "Bad Password"
    COORDINATES = "Bad Coordinates"
    BAD_BALANCE = "Bad Coin Balance"
    BAD_FOLLOWER = "Bad Follower ID"
    BAD_TOKEN = "Bad User Token"
    IMAGE_ERROR = "Image Error"
    BAD_INPUT = "Bad Input"
    BAD_CREDENTIALS = "Bad Credentials"
    PASSWORD_RESET = "Bad Password Reset Box"




class ExceptionReasonEnum(StrEnum):
    MISSING_VALUE = "Missing Value"
    INCORRECT_VALUE = "Incorrect Value"
    VALUE_IN_USE = "Value Already In Use"
    DUPLICATE_VALUE = "Duplicate Value"
    SELF_ACTION = "Cannot Perform Action On Self"
    LOGIC_ERROR = "Logic Error"
    LOW_BALANCE = "Low Coin Balance"
    INCORRECT_TOKEN = "Incorrect Token"
    ONLY_ONE_ITEM = "Only 1 Item Allowed"
    NOT_CONFIRMED = "Email Not Confirmed"
    CHANGE_REQUESTED = "Change Requested"
    NUMBER_MUST_PRESENT = "Should Contain Numbers"
    SIX_CHARS_AT_LEAST = "Should Be 6 Symbols At Least"



class Exc:
    @staticmethod
    def prepare(message, reasons) -> tuple:
        if isinstance(reasons, str):
            reasons = (reasons,)
        if not message:
            message = " .".join(reasons)
        return message, reasons

    @classmethod
    def value(
        cls,
        message: str | None = None,
        of_group: str = "Unknown Error",
        reasons="",
    ):
        message, reasons = cls.prepare(message, reasons)
        raise GraphQLError(
            message,
            extensions={
                "type": "Value Error",
                "exception_group": of_group,
                "reasons": reasons,
            },
        )

    @classmethod
    def missing_data(
        cls,
        message: str | None = None,
        of_group: str = "Unknown Error",
        reasons: Tuple[str] | str = "",
    ):
        message, reasons = cls.prepare(message, reasons)
        raise GraphQLError(
            message,
            extensions={
                "type": "No Value Provided Error",
                "exception_group": of_group,
                "reasons": reasons,
            },
        )

    @classmethod
    def low_wallet(
        cls,
        message: str | None = None,
        of_group: str = "Unknown Error",
        reasons = "",
    ):
        message, reasons = cls.prepare(message, reasons)
        raise GraphQLError(
            message,
            extensions={
                "type": "Not Enough Coins",
                "exception_group": of_group,
                "reasons": reasons,
            },
        )
