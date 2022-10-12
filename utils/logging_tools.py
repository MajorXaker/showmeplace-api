import json

from alchql.query_helper import QueryHelper

from utils.config import log


async def debug_log(cls, info):
    qh = QueryHelper.get_current_field(info)
    raw_headers = [
        [line.decode("utf-8") for line in hd] for hd in info.context.request.headers.raw
    ]
    headers = {ln[0]: ln[1] for ln in raw_headers if ln[0] == "authorization"}
    data = json.dumps(
        {
            "query": str(cls),
            "headers": headers,
            "variables": info.variable_values,
            "requested_data": [x.name for x in qh.values],
        }
    )
    log.debug(data)
