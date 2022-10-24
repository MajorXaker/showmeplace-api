import random

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


from models.db_models import User, Place, Category
from utils.db import db_url

LONGITUDE_MIN = -180
LONGITUDE_MAX = 179
LATITUDE_MIN = -60
LATITUDE_MAX = 60
LONGITUDE_STEP = 4
LATITUDE_STEP = 2


def progress(value, from_min, from_max):
    to_min, to_max = 1, 100
    # Figure out how 'wide' each range is
    left_span = from_max - from_min
    right_span = to_max - to_min
    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - from_min) / float(left_span)
    # Convert the 0-1 range into a value in the right range.
    raw_result = to_min + (value_scaled * right_span)
    return int(raw_result)


def spam():
    engine = create_engine(db_url)
    with Session(engine) as session:
        spammer = session.execute(
            sa.insert(User)
            .values(
                {
                    User.name: "Mr.Everywhere",
                    User.external_id: "asodifa[dkojfaidfjpaiu",
                    User.external_id_type: "META",
                }
            )
            .returning(User.id)
        ).fetchone()

        categories_ids = [cat.id for cat in session.execute(sa.select(Category.id))]

        i = 1
        for long in range(LONGITUDE_MIN, LONGITUDE_MAX, LONGITUDE_STEP):
            for lat in range(LATITUDE_MIN, LATITUDE_MAX, LATITUDE_STEP):
                crd = (long, lat)

                session.execute(
                    sa.insert(Place).values(
                        {
                            Place.name: f"Spammed place {i}",
                            Place.description: f"Coords {crd}",
                            Place.category_id: random.choice(categories_ids),
                            Place.coordinate_longitude: long,
                            Place.coordinate_latitude: lat,
                            Place.owner_id: spammer.id,
                        }
                    )
                )
                i += 1
            print(f"Progress: {progress(long, LONGITUDE_MIN, LONGITUDE_MAX)}")
        session.commit()
    print("Places has been spammed")


if __name__ == "__main__":
    spam()
