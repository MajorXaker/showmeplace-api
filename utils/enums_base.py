from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.value!r}"

    @classmethod
    def __iter__(cls):
        for i in cls:
            yield cls(i)
