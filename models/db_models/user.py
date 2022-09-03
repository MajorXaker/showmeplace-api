import sqlalchemy as sa

from models.base_engine import Model


class User(Model):

    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    has_onboarded = sa.Column(sa.Boolean)
    level = sa.Column(sa.Integer)
    coins = sa.Column(sa.Integer)
    description = sa.Column(sa.Text)

