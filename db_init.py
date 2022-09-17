#!/usr/bin/env python3

import models.db_models as m
from sqlalchemy import create_engine

from utils.config import settings as s
from utils.db import db_url

BASELESS_DB = (
    "postgresql://"
    f"{s.DATABASE_USER}:"
    f"{s.DATABASE_PASSWORD}@"
    f"{s.DATABASE_HOST}:"
    f"{s.DATABASE_PORT}"
)

DB_URL = (
    "postgresql://"
    f"{s.DATABASE_USER}:"
    f"{s.DATABASE_PASSWORD}@"
    f"{s.DATABASE_HOST}:"
    f"{s.DATABASE_PORT}/"
    f"{s.DATABASE_DB}"
)


def check_test_db(db_url):
    if not any(i in db_url for i in ("localhost", "127.0.0.1", "@postgres")):
        print(db_url)
        raise Exception("Use local database only!")


def setup_db_for_tests():
    check_test_db(db_url)
    e = create_engine(BASELESS_DB)

    conn = e.connect()
    conn.execute("commit")
    conn.execute(f"DROP DATABASE IF EXISTS {s.DATABASE_DB}")
    conn.execute("commit")
    conn.execute(f"CREATE DATABASE {s.DATABASE_DB}")
    conn.execute("commit")
    conn.close()

    e = create_engine(db_url)
    e.connect().execute("CREATE EXTENSION pg_trgm")
    e.connect().execute("CREATE EXTENSION unaccent")
    m.Model.metadata.create_all(e)


if __name__ == "__main__":
    setup_db_for_tests()
