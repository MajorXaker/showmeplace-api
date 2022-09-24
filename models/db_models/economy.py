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

    @classmethod
    async def execute(
        cls,
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
            new_coin_value = user_coins - action.change_amount
            sign = "-"
            if new_coin_value < 0:
                raise cls.InsufficientCoins("Not enough coins")

        await session.execute(
            sa.update(User)
            .where(User.id == coin_receiver_user_id)
            .values({User.coins: new_coin_value})
        )

        return {
            "change_amount": f"{sign}{action.change_amount}",
            "coins": new_coin_value,
        }

    @staticmethod
    async def verify_possibility(
        session: AsyncSession,
        user_id: int,
        action_names: list
        | None = None,  # if there is no action names - then check all
    ):
        actions = (
            await session.execute(
                sa.select(
                    ActionsEconomy.action_name,
                    ActionsEconomy.change_type,
                    ActionsEconomy.change_amount,
                )
            )
        ).fetchall()
        user_wallet = (
            (await session.execute(sa.select(User.coins).where(User.id == user_id)))
            .fetchone()
            .coins
        )
        if not action_names:
            action_names = [action.action_name for action in actions]
        always_true = {
            action.action_name: True
            for action in actions
            if all(
                [
                    action.action_name in action_names,
                    action.change_type == CoinValueChangeEnum.EARN,
                ]
            )
        }
        possibilities = {
            action.action_name: (user_wallet - action.change_amount) > 0
            for action in actions
            if all(
                [
                    action.action_name in action_names,
                    action.change_type == CoinValueChangeEnum.SPEND,
                ]
            )
        }
        return {**always_true, **possibilities}

    class InsufficientCoins(Exception):
        pass
