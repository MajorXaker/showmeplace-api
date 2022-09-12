import sqlalchemy as sa

from models.base_engine import Model

# TODO presigned url + its date
class PlaceImage(Model):
    __tablename__ = "place_image"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    place_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("place.id", ondelete="RESTRICT"),
        # index=True,
        # nullable=False,
    )
    s3_filename = sa.Column(sa.Text)
    description = sa.Column(sa.Text)
