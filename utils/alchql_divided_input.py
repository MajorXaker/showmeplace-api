from typing import List

from alchql.get_input_type import get_input_fields
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta


class DividedInputRow(BaseModel):
    # example {"model": User, "only_fields": ["id"], "required_fields": ["id"], prefix: "place"}
    model: DeclarativeMeta
    only_fields: List[str]
    exclude_fields: List[str] | None
    required_fields: List[str] | None
    prefix: str

    class Config:
        arbitrary_types_allowed = True

    # TODO this
    # @validator("only fields or excluded fields")
    # def onlyfields_requiredfields(cls, v):

    # @validator("model")
    # def is_declarative(cls, v):
    #     if not isinstance(v, DeclarativeMeta):
    #         raise ValueError(f"Model must be a {DeclarativeMeta} class")
    #     return v


def divided_inputs(data: List[DividedInputRow]):
    cooked_inputs = {}
    emtptyable_fields = ["exclude_fields", "required_fields", "only_fields"]
    for model_input in data:
        for field in emtptyable_fields:
            if not getattr(model_input, field):
                setattr(model_input, field, [])
        precooked_fields = get_input_fields(
            model=model_input.model,
            only_fields=model_input.only_fields,
            exclude_fields=model_input.exclude_fields,
            required_fields=model_input.required_fields,
        )
        for field_name, value in precooked_fields.items():
            cooked_inputs[f"{model_input.prefix}_{field_name}"] = value

    return cooked_inputs