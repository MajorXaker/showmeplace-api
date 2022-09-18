from alembic import op
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.db_models import Category, ActionsEconomy
from utils.db import db_url


def insert_categories(session):

    data = [
        {"name": "Food"},
        {"name": "Rest"},
        {"name": "Nature"},
        {"name": "Culture"},
        {"name": "Kids"},
        {"name": "Beauty"},
        {"name": "Sport"},
        {"name": "Creative activities"},
        {"name": "Nightlife"},
        {"name": "Pets"},
        # {"name": "Auto"}, # :'(
    ]

    return [
        session.execute(
            sa.insert(Category)
            .values({Category.name: val["name"]})
            .returning(Category.id)
        )
        .fetchone()
        .id
        for val in data
    ]


def insert_economy(session):

    data = [
        {"action_name": "Visit a place", "change_type": "EARN", "change_amount": 10},
        {"action_name": "Create a place", "change_type": "EARN", "change_amount": 25},
        {"action_name": "Share a profile", "change_type": "EARN", "change_amount": 25},
        {"action_name": "Share a place", "change_type": "EARN", "change_amount": 10},
        {
            "action_name": "Have your place visited",
            "change_type": "EARN",
            "change_amount": 5,
        },
        {
            "action_name": "Have your secret place visited",
            "change_type": "EARN",
            "change_amount": 35,
        },
        {
            "action_name": "Have your secret place opened",
            "change_type": "EARN",
            "change_amount": 25,
        },
        {
            "action_name": "Open a secret place",
            "change_type": "SPEND",
            "change_amount": 500,
        },
        {
            "action_name": "Create first secret place",
            "change_type": "SPEND",
            "change_amount": 50,
        },
        {
            "action_name": "Create a new place of the same category",
            "change_type": "SPEND",
            "change_amount": 50,
        },
        {
            "action_name": "Create new secret place",
            "change_type": "SPEND",
            "change_amount": 1000,
        },
    ]

    return [
        session.execute(
            sa.insert(ActionsEconomy)
            .values(
                {
                    ActionsEconomy.action_name: val["action_name"],
                    ActionsEconomy.change_type: val["change_type"],
                    ActionsEconomy.change_amount: val["change_amount"],
                }
            )
            .returning(ActionsEconomy.id)
        )
        .fetchone()
        .id
        for val in data
    ]


if __name__ == "__main__":
    engine = create_engine(db_url)
    with Session(engine) as session:
        economy_ids = insert_economy(session)
        category_ids = insert_categories(session)
        aaa = 5
