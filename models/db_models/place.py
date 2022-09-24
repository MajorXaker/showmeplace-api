import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base_engine import Model, RecordTimestampFields


class Place(Model, RecordTimestampFields):

    __tablename__ = "place"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    # todo photo field or relation
    description = sa.Column(sa.Text)
    coordinate_longitude = sa.Column(sa.Float, nullable=False)
    coordinate_latitude = sa.Column(sa.Float, nullable=False)
    address = sa.Column(sa.Text)
    category_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("category.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )

    is_secret_place = sa.Column(sa.Boolean, server_default="FALSE")
    active_due_date = sa.Column(sa.DateTime)
    owner_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    # secret_extra_id = sa.Column(
    #     sa.Integer,
    #     sa.ForeignKey("secret_extras.id", ondelete=""),
    #     index=True,
    #     nullable=False,
    # )
    # TODO SECRET PLACE EXTRA id here

    # todo place merge
    # merge would be as a new entity - grouped place
