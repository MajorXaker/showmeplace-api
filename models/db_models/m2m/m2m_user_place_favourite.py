import sqlalchemy as sa

from models.base_engine import Model, RecordTimestampFields


class M2MUserPlaceFavourite(Model, RecordTimestampFields):
    __tablename__ = "m2m_user_place_favourite"

    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    place_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("place.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (
        sa.PrimaryKeyConstraint(
            user_id, place_id, name="m2m_user_place_favourite_pkey"
        ),
        # sa.UniqueConstraint(description_id, image_id, name="_unique_ordering"),
    )
