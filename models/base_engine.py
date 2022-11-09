from datetime import datetime

import sqlalchemy as _sa
from sqlalchemy import MetaData
from sqlalchemy.orm import as_declarative


class RecordTimestampFields:
    """
    Collection of record edition timestamps
    They are common for many models
    """

    record_created = _sa.Column(
        _sa.DateTime,
        nullable=False,
        default=datetime.now,
        server_default=_sa.text("statement_timestamp()"),
    )

    record_modified = _sa.Column(
        _sa.DateTime,
        nullable=False,
        default=datetime.now,
        server_default=_sa.text("statement_timestamp()"),
        onupdate=datetime.now,
        index=True,
    )

    def get_record_timestamps(self):
        return (
            "created @ {:%Y-%m-%d %H:%M:%S},"
            " modified @ {:%Y-%m-%d %H:%M:%S}".format(
                self.record_created,
                self.record_modified,
            )
        )


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


@as_declarative(metadata=MetaData(naming_convention=convention))
class Model:
    metadata: MetaData
