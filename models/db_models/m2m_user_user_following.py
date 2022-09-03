import sqlalchemy as sa

from models.base_engine import Model
from models.db_models.user import User


class M2MUserFollowingUser(Model):
    __tablename__ = "m2m_user_place_favourite"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    follower_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    lead_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (
        sa.PrimaryKeyConstraint(
            lead_id, follower_id, name="m2m_user_place_favourite_pkey"
        ),
        # sa.UniqueConstraint(description_id, image_id, name="_unique_ordering"),
    )
