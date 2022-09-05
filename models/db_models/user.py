import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base_engine import Model


class User(Model):

    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    has_onboarded = sa.Column(sa.Boolean, default=False, server_default="FALSE")
    level = sa.Column(sa.Integer)
    coins = sa.Column(sa.Integer)
    description = sa.Column(sa.Text)

    place_marked = relationship(
        "Place",
        secondary="M2MUserPlaceMarked",
        viewonly=True,
    )
    place_favourited = relationship(
        "Place",
        secondary="M2MUserPlaceFavourite",
        viewonly=True,
    )
    place_visited = relationship(
        "Place",
        secondary="M2MUserPlaceVisited",
        viewonly=True,
    )
    secret_place_opened = relationship(
        "Place",
        secondary="M2MUserSecretPlace",
        viewonly=True,
    )
    user_followed = relationship(
        "User",
        secondary="M2MUserFollowingUser",
        viewonly=True,
        remote_side="lead_id"
    )
    user_following = relationship(
        "User",
        secondary="M2MUserFollowingUser",
        viewonly=True,
        remote_side="follower_id"
    )
