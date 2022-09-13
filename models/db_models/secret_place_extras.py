import sqlalchemy as sa

from models.base_engine import Model, RecordTimestampFields


class SecretPlaceExtra(Model, RecordTimestampFields):

    __tablename__ = "secret_extras"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    food_suggestion = sa.Column(sa.Text)
    time_suggestion = sa.Column(sa.Text)
    company_suggestion = sa.Column(sa.Text)
    music_suggestion = sa.Column(sa.Text)
    extra_suggestion = sa.Column(sa.Text)
    place_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("place.id", ondelete="CASCADE"),
        nullable=True,
    )
