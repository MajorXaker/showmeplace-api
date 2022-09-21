import sqlalchemy as sa

from models.base_engine import Model, RecordTimestampFields


class M2MUserFollowingUser(Model, RecordTimestampFields):
    __tablename__ = "m2m_user_user_following_user"

    follower_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    lead_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (
        sa.PrimaryKeyConstraint(lead_id, follower_id, name="m2m_user_following_user"),
        # sa.UniqueConstraint(description_id, image_id, name="_unique_ordering"),
    )
