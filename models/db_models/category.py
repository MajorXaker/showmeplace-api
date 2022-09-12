import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base_engine import Model


class Category(Model):

    __tablename__ = "category"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    # places = relationship("Place", back_populates='place_category')
