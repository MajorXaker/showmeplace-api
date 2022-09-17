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
    # todo place merge

    #
    # user_marked = relationship(
    #     "User",
    #     secondary="m2m_user_place_marked",
    #     # viewonly=True,
    #     # backref="Place"
    # )

    # user_visited = relationship(
    #     "User",
    #     secondary="M2MUserPlaceVisited",
    #     viewonly=True,
    # )
    # user_favourited = relationship(
    #     "User",
    #     secondary="M2MUserPlaceFavourite",
    #     viewonly=True,
    # )
    # user_secret_place_opened = relationship(
    #     "User",
    #     secondary="M2MUserSecretPlace",
    #     viewonly=True,
    # )
