import sqlalchemy as sa

from models.base_engine import Model
from models.db_models.place import Place
from models.db_models.user import User


class M2MUserPlaceFavourite(Model):
    __tablename__ = "m2m_user_place_favourite"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    place_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Place.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (
        sa.PrimaryKeyConstraint(
            user_id, place_id, name="m2m_user_place_favourite_pkey"
        ),
        # sa.UniqueConstraint(description_id, image_id, name="_unique_ordering"),
    )
