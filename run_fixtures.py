from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fixtures.fixtures import insert_categories, insert_economy, insert_category_images
from utils.db import db_url

if __name__ == "__main__":
    engine = create_engine(db_url)
    with Session(engine) as session:
        economy_ids = insert_economy(session)
        category_ids = insert_categories(session)
        cat_img_ids = insert_category_images(session)
        session.commit()
    aaa = 5
