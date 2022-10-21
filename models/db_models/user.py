import sqlalchemy as sa

from models.base_engine import Model, RecordTimestampFields
from models.enums import IdentificationEnum


class User(Model, RecordTimestampFields):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    level = sa.Column(sa.Integer)
    coins = sa.Column(sa.Integer)
    description = sa.Column(sa.Text)
    external_id = sa.Column(sa.Text, nullable=False)
    external_id_type: IdentificationEnum = sa.Column(
        sa.Text, nullable=False, server_default="COGNITO"
    )
    active_email_address_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("email_address.id", ondelete="RESTRICT"),
        nullable=True,
    )
    # TODO what do we need for profile sharing - Ougen**
    # Mutation for generation UID which will live for X (in settings) hours.
    # TODO URL Endpoint for such page
