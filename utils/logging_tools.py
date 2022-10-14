import json

from alchql.query_helper import QueryHelper

from utils.config import log


async def debug_log(cls, info):
    qh = QueryHelper.get_current_field(info)
    raw_headers = [
        [line.decode("utf-8") for line in hd] for hd in info.context.request.headers.raw
    ]
    headers = {ln[0]: ln[1] for ln in raw_headers if ln[0] == "authorization"}

    data = {
        "variables": info.variable_values,
        "query": str(cls),
        "headers": headers,
        "requested_data": [x.name for x in qh.values],
    }
    if "sort" in info.variable_values:
        data["variables"]["sort"] = [
            str(sort_val) for sort_val in info.variable_values["sort"]
        ]

    log.debug(json.dumps(data))
