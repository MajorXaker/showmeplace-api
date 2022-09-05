import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base_engine import Model


class Place(Model):

    __tablename__ = "place"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    # todo photo field or relation
    description = sa.Column(sa.Text)
    coordinate_longitude = sa.Column(sa.Float, nullable=False)
    coordinate_latitude = sa.Column(sa.Float, nullable=False)
    address = sa.Column(sa.String)
    category_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("place_category.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    is_secret_place = sa.Column(sa.Boolean, server_default="FALSE")
    # todo place merge
    secret_place_extras = sa.Column(
        sa.Integer,
        sa.ForeignKey("place_category.id", ondelete="RESTRICT"),
        nullable=False,
    )

    user_marked = relationship(
        "User",
        secondary="M2MUserPlaceMarked",
        viewonly=True,
    )

    user_visited = relationship(
        "User",
        secondary="M2MUserPlaceVisited",
        viewonly=True,
    )
    user_favourited = relationship(
        "User",
        secondary="M2MUserPlaceFavourite",
        viewonly=True,
    )
    user_secret_place_opened = relationship(
        "User",
        secondary="M2MUserSecretPlace",
        viewonly=True,
    )
