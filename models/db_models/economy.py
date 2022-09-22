from sqlalchemy.ext.asyncio import AsyncSession

from models.base_engine import Model, RecordTimestampFields
import sqlalchemy as sa

from models.db_models import User
from models.enums import CoinValueChangeEnum


class ActionsEconomy(Model, RecordTimestampFields):
    __tablename__ = "actions_economy"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    action_name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.Text)
    change_type: CoinValueChangeEnum = sa.Column(sa.String, nullable=False)
    change_amount = sa.Column(sa.Integer, nullable=False, server_default="0")

    @staticmethod
    async def execute(
        session: AsyncSession,
        action_name: str,
        coin_receiver_user_id: int,
    ):

        action = (
            await session.execute(
                sa.select(
                    ActionsEconomy.action_name,
                    ActionsEconomy.change_type,
                    ActionsEconomy.change_amount,
                ).where(ActionsEconomy.action_name == action_name)
            )
        ).fetchone()

        user_coins = (
            (
                await session.execute(
                    sa.select(User.coins).where(User.id == coin_receiver_user_id)
                )
            )
            .fetchone()
            .coins
        )

        if action.change_type == "EARN":
            new_coin_value = user_coins + action.change_amount
            sign = ""
        else:
            new_coin_value = user_coins + action.change_amount
            sign = "-"

        await session.execute(
            sa.update(User)
            .where(User.id == coin_receiver_user_id)
            .values({User.coins: new_coin_value})
        )

        return {
            "change_amount": f"{sign}{action.change_amount}",
            "coins": new_coin_value,
        }
