import sqlalchemy as sa

from models.db_models import Category, ActionsEconomy, CategoryImage


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
        {"name": "Secret place", "mark": "secret"},
        # {"name": "Auto"}, # :'(
    ]

    return [
        session.execute(
            sa.insert(Category)
            .values({Category.name: val["name"], Category.mark: val.get("mark", None)})
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


def insert_category_images(session):
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

    ids = []
    for img, category in zip(data, categories):
        category_id = (
            session.execute(
                sa.select(Category.id).where(Category.name == category["name"])
            )
            .fetchone()
            .id
        )
        assert category_id is not None

        id_pin = (
            session.execute(
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
            .fetchone()
            .id
        )

        id_icon = (
            session.execute(
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
            .fetchone()
            .id
        )
        ids.append((id_pin, id_icon))

    return ids
