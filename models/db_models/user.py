import sqlalchemy as sa
from sqlalchemy.orm import relationship

# from models.db_models.m2m.m2m_user_user_following import M2MUserFollowingUser
# from models.db_models.m2m.m2m_user_place_favourite import M2MUserPlaceFavourite
from models.db_models.m2m.m2m_user_place_marked import M2MUserPlaceMarked
# from models.db_models.m2m.m2m_user_place_visited import M2MUserPlaceVisited
# from models.db_models.m2m.m2m_user_secret_place import M2MUserOpenedSecretPlace
from models.base_engine import Model


# from models.db_models import M2MUserPlaceMarked, M2MUserPlaceFavourite, M2MUserSecretPlace, M2MUserFollowingUser
# from models.db_models.m2m_user_place_visited import M2MUserPlaceVisited


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
        secondary="m2m_user_place_marked",
        backref="user",
        viewonly=True,
    )
    # place_favourited = relationship(
    #     "Place",
    #     secondary=M2MUserPlaceFavourite,
    #     viewonly=True,
    # )
    # place_visited = relationship(
    #     "Place",
    #     secondary=M2MUserPlaceVisited,
    #     viewonly=True,
    # )
    # secret_place_opened = relationship(
    #     "Place",
    #     secondary=M2MUserOpenedSecretPlace,
    #     viewonly=True,
    # )
    # user_leading = relationship(
    #     "User",
    #     secondary=M2MUserFollowingUser,
    #     viewonly=True,
    #     remote_side="lead_id"
    # )
    # user_following = relationship(
    #     "User",
    #     secondary=M2MUserFollowingUser,
    #     viewonly=True,
    #     remote_side="follower_id"
    # )
