import re
from functools import reduce

import sqlalchemy as sa


def parse_query(query):
    subqueries = [
        sa.func.to_tsquery(
            sa.func.querytree(sa.func.plainto_tsquery(token)).concat(":*")
        )
        for token in re.split(r"[^\w\d\\/\.]+", query, flags=re.UNICODE)
        if token.strip()
    ]
    if not subqueries:
        return

    combined_query = reduce(
        lambda cq, q: cq.op("&&", precedence=100)(q),
        subqueries,
    )
    return combined_query.self_group()
