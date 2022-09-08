import sqlalchemy as sa

from models.base_engine import Model
# from models.db_models.place import Place
# from models.db_models.user import User


# M2MUserPlaceMarked = sa.Table(
#     "m2m_user_place_marked",
#     Model.metadata,
#     sa.Column("user_id", sa.Integer, nullable=False, index=True),
#     sa.Column("place_id", sa.Integer, nullable=False, index=True),
#     sa.PrimaryKeyConstraint(
#         "user_id", "place_id", name="m2m_user_place_marked_pkey"
#     ),
#     sa.ForeignKeyConstraint(
#         ("user_id",),
#         ["user.id"],
#         onupdate="CASCADE",
#         ondelete="CASCADE",
#     ),
#     sa.ForeignKeyConstraint(
#         ("place_id",),
#         ["place.id"],
#         onupdate="CASCADE",
#         ondelete="CASCADE",
#     ),
# )
#
# class M2MUserPlaceMarked(Model):
#     __tablename__ = "m2m_user_place_marked"
#
#     user_id = sa.Column(
#         sa.Integer,
#         sa.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
#         nullable=False,
#     )
#     place_id = sa.Column(
#         sa.Integer,
#         sa.ForeignKey("place.id", onupdate="CASCADE", ondelete="CASCADE"),
#         nullable=False,
#     )
#     __table_args__ = (
#         sa.PrimaryKeyConstraint(
#             user_id, place_id, name="m2m_user_place_ownership_pkey"
#         ),
#         # sa.UniqueConstraint(description_id, image_id, name="_unique_ordering"),
#     )
