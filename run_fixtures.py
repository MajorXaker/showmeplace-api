from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fixtures.fixtures import insert_data
from utils.db import db_url

if __name__ == "__main__":
    engine = create_engine(db_url)
    with Session(engine) as session:
        insert_data(session)
    print("Fixtures has been applied")
