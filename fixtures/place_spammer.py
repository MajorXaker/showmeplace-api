import random

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


from models.db_models import User, Place
from utils.db import db_url


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

        i = 1
        for long in range(-180, 180, 4):
            for lat in range(-60, 60, 2):
                crd = (long, lat)

                session.execute(
                    sa.insert(Place).values(
                        {
                            Place.name: f"Spammed place {i}",
                            Place.description: f"Coords {crd}",
                            Place.category_id: random.randint(1, 11),
                            Place.coordinate_longitude: long,
                            Place.coordinate_latitude: lat,
                            Place.owner_id: spammer.id,
                        }
                    )
                )
                i += 1

        session.commit()
    print("Places has been spammed")


if __name__ == "__main__":
    spam()
