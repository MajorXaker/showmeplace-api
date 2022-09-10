import sqlalchemy as sa

from models.base_engine import Model

# from models.db_models.user import User


# M2MUserFollowingUser = sa.Table(
#     "m2m_user_user_following_user",
#     Model.metadata,
#     sa.Column("follower_id", sa.Integer, nullable=False, index=True),
#     sa.Column("lead_id", sa.Integer, nullable=False, index=True),
#     sa.PrimaryKeyConstraint(
#         "follower_id", "lead_id", name="m2m_user_user_following_user"
#     ),
#     sa.ForeignKeyConstraint(
#         ("follower_id",),
#         ["user.id"],
#         onupdate="CASCADE",
#         ondelete="CASCADE",
#     ),
#     sa.ForeignKeyConstraint(
#         ("lead_id",),
#         ["user.id"],
#         onupdate="CASCADE",
#         ondelete="CASCADE",
#     ),
#
# )

class M2MUserFollowingUser(Model):
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
        sa.PrimaryKeyConstraint(
            lead_id, follower_id, name="m2m_user_following_user"
        ),
        # sa.UniqueConstraint(description_id, image_id, name="_unique_ordering"),
    )
