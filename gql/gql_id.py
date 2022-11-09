import base64
import json
from typing import Tuple, Union


def decode_gql_id(encoded_id: str) -> Tuple[str, Union[str, int]]:
    type_name, id_text = base64.b64decode(encoded_id).decode().split(":")
    # TODO - failsafe when token is incorrect - OUGEN
    return type_name, json.loads(id_text)


def encode_gql_id(type_: str, id_: Union[str, int]) -> str:
    """

    @param type_: SomethingType - denotes a type of a value
    @param id_: ID of a value in the database
    @return: b64 coded SomethingType:5
    """
    text = f"{type_}:{json.dumps(id_)}"
    return base64.b64encode(text.encode()).decode()


def assert_gql_id(coded_id: str, data_type: str = None, id_: str | int = None):
    assert data_type or id_
    data = decode_gql_id(coded_id)
    if data_type:
        assert data[0] == data_type
    if id_:
        assert data[1] == id_
