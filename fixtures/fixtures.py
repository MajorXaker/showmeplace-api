import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.db_models import Category, ActionsEconomy, CategoryImage
from utils.db import db_url


def insert_categories():
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
        {"name": "Secret place", "mark": "secret"},
        # {"name": "Auto"}, # :'(
    ]

    return [
        sa.insert(Category)
        .values({Category.name: val["name"], Category.mark: val.get("mark", None)})
        .returning(Category.id)
        for val in data
    ]


def insert_economy():
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
        sa.insert(ActionsEconomy)
        .values(
            {
                ActionsEconomy.action_name: val["action_name"],
                ActionsEconomy.change_type: val["change_type"],
                ActionsEconomy.change_amount: val["change_amount"],
            }
        )
        .returning(ActionsEconomy.id)
        for val in data
    ]


def insert_category_images_sync(session):
    data = [
        {"name": "Food"},
        {"name": "Rest"},
        {"name": "Nature"},
        {"name": "Culture"},
        {"name": "Kids"},
        {"name": "Beauty"},
        {"name": "Sport"},
        {"name": "Creative"},
        {"name": "Nightlife"},
        {"name": "Pets"},
        {"name": "Secret_opened"},
        {"name": "Secret_closed"},
    ]
    categories = [
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
        {"name": "Secret place"},
        {"name": "Secret place"},
    ]

    queries = []
    for img, category in zip(data, categories):
        category_id = (
            session.execute(
                sa.select(Category.id).where(Category.name == category["name"])
            )
            .fetchone()
            .id
        )
        assert category_id is not None

        pin_q = (
            sa.insert(CategoryImage)
            .values(
                {
                    CategoryImage.s3_filename: f'{img["name"]}.png',
                    CategoryImage.s3_path: "category_images/pins/",
                    CategoryImage.description: "pin",
                    CategoryImage.category_id: category_id,
                }
            )
            .returning(CategoryImage.id)
        )

        icon_q = (
            sa.insert(CategoryImage)
            .values(
                {
                    CategoryImage.s3_filename: f'{img["name"]}.png',
                    CategoryImage.s3_path: "category_images/icons/",
                    CategoryImage.description: "icon",
                    CategoryImage.category_id: category_id,
                }
            )
            .returning(CategoryImage.id)
        )

        decaying_q = (
            sa.insert(CategoryImage)
            .values(
                {
                    CategoryImage.s3_filename: f'{img["name"]}.png',
                    CategoryImage.s3_path: "category_images/decay/",
                    CategoryImage.description: "pin_decay",
                    CategoryImage.category_id: category_id,
                }
            )
            .returning(CategoryImage.id)
        )

        queries.append(pin_q)
        queries.append(icon_q)
        queries.append(decaying_q)

    return queries


# TODO finish this prototype
# async def insert_category_images_async(session):
#     data = [
#         {"name": "Food"},
#         {"name": "Rest"},
#         {"name": "Nature"},
#         {"name": "Culture"},
#         {"name": "Kids"},
#         {"name": "Beauty"},
#         {"name": "Sport"},
#         {"name": "Creative"},
#         {"name": "Nightlife"},
#         {"name": "Pets"},
#         {"name": "Secret_opened"},
#         {"name": "Secret_closed"},
#     ]
#     categories = [
#         {"name": "Food"},
#         {"name": "Rest"},
#         {"name": "Nature"},
#         {"name": "Culture"},
#         {"name": "Kids"},
#         {"name": "Beauty"},
#         {"name": "Sport"},
#         {"name": "Creative activities"},
#         {"name": "Nightlife"},
#         {"name": "Pets"},
#         {"name": "Secret place"},
#         {"name": "Secret place"},
#     ]
#
#     queries = []
#     for img, category in zip(data, categories):
#         category_id = await (
#             session.execute(
#                 sa.select(Category.id).where(Category.name == category["name"])
#             )
#             .fetchone()
#             .id
#         )
#         assert category_id is not None
#
#         pin_q = (
#             sa.insert(CategoryImage)
#             .values(
#                 {
#                     CategoryImage.s3_filename: f'{img["name"]}.png',
#                     CategoryImage.s3_path: "category_images/pins/",
#                     CategoryImage.description: "pin",
#                     CategoryImage.category_id: category_id,
#                 }
#             )
#             .returning(CategoryImage.id)
#         )
#
#         icon_q = (
#             sa.insert(CategoryImage)
#             .values(
#                 {
#                     CategoryImage.s3_filename: f'{img["name"]}.png',
#                     CategoryImage.s3_path: "category_images/icons/",
#                     CategoryImage.description: "icon",
#                     CategoryImage.category_id: category_id,
#                 }
#             )
#             .returning(CategoryImage.id)
#         )
#
#         decaying_q = (
#             sa.insert(CategoryImage)
#             .values(
#                 {
#                     CategoryImage.s3_filename: f'{img["name"]}.png',
#                     CategoryImage.s3_path: "category_images/decay/",
#                     CategoryImage.description: "pin_decay",
#                     CategoryImage.category_id: category_id,
#                 }
#             )
#             .returning(CategoryImage.id)
#         )
#
#         queries.append((pin_q, icon_q, decaying_q))
#
#     return queries


def insert_data(session):
    economy = [session.execute(q).fetchone().id for q in insert_categories()]
    categories = [session.execute(q).fetchone().id for q in insert_economy()]
    images = [
        session.execute(q).fetchone().id for q in insert_category_images_sync(session)
    ]
    session.commit()


if __name__ == "__main__":
    engine = create_engine(db_url)
    with Session(engine) as session:
        insert_data(session)
    print("Fixtures has been applied")
