from typing import Tuple

from graphql import GraphQLError

from utils.enums_base import StrEnum


class ExceptionEnum(StrEnum):
    EMAIL = "Bad Email"
    PASSWORD = "Bad Password"
    COORDINATES = "Bad Coordinates"
    LOW_BALANCE = "Low Coin Balance"


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
        reasons: Tuple[str] | str = "",
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
