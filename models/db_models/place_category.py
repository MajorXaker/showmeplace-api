import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base_engine import Model


class PlaceCategory(Model):

    __tablename__ = "place_category"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    places = relationship("Place")
    # TODO icon field
