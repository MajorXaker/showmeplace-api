import sqlalchemy as sa

from models.base_engine import Model, RecordTimestampFields
from models.enums import EmailStatusEnum


class EmailAddress(Model, RecordTimestampFields):
    __tablename__ = "email_address"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    address = sa.Column(sa.String)
    status = sa.Column(
        sa.String, server_default=EmailStatusEnum.PENDING, nullable=False, index=True
    )
