from models.base_engine import Model, RecordTimestampFields
import sqlalchemy as sa

from models.enums import CoinValueChangeEnum


class ActionsEconomy(Model, RecordTimestampFields):
    __tablename__ = "actions_economy"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    action_name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.Text)
    change_type: CoinValueChangeEnum = sa.Column(sa.String, nullable=False)
    change_amount = sa.Column(sa.Integer, nullable=False, server_default="0")
