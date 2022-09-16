from models.base_engine import Model, RecordTimestampFields
import sqlalchemy as sa

from models.enums import CoinValueChangeEnum


class CoinsEconomy(Model, RecordTimestampFields):
    __tablename__ = "coins_economy"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    description = sa.Column(sa.Text)
    change_type: CoinValueChangeEnum = sa.Column(sa.String, nullable=False)
    change_amount = sa.Column(sa.Integer)
