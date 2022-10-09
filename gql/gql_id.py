import base64
import json
from typing import Tuple, Union


def decode_gql_id(encoded_id: str) -> Tuple[str, Union[str, int]]:
    type_name, id_text = base64.b64decode(encoded_id).decode().split(":")
    return type_name, json.loads(id_text)


def encode_gql_id(type_: str, id_: Union[str, int]) -> str:
    text = f"{type_}:{json.dumps(id_)}"
    return base64.b64encode(text.encode()).decode()

def gql_decoder(func):
    def wrapper_decoder(gql_coded_id):
        decoded_id = decode_gql_id(gql_coded_id)
        func(decoded_id)
    return wrapper_decoder
