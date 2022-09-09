#!/usr/bin/env python3
import csv
import json
from typing import Optional
from urllib.parse import urlparse

import sqlalchemy as sa
from pydantic import BaseModel, validator
from sqlalchemy import create_engine
import models.db_models as models


from utils.db import db_url

URL = urlparse(db_url)
HOSTNAME = URL.hostname
DATABASE_DB = URL.path[1:]
DATABASE_URL = URL._replace(path="").geturl()


def install_fixture_sql(engine, filename):
    with open(filename) as f:
        print(f"Apply fixture {filename}")

        for i in f.readlines():
            engine.execute(i)
        engine.execute("commit")


def setup_db_for_tests():
    if HOSTNAME not in ("127.0.0.1", "localhost"):
        raise Exception(f"Invalid hostname: {HOSTNAME}")

    e = create_engine(DATABASE_URL)

    conn = e.connect()
    conn.execute("commit")
    conn.execute(f"DROP DATABASE IF EXISTS {DATABASE_DB}")
    conn.execute("commit")
    conn.execute(f"CREATE DATABASE {DATABASE_DB}")
    conn.execute("commit")
    conn.close()

    e = create_engine(DATABASE_URL)

    e.connect().execute("CREATE EXTENSION pg_trgm")
    e.connect().execute("CREATE EXTENSION unaccent")

    models.Model.metadata.create_all(e)

    install_fixture_sql(e, "fixtures/place_category.sql")


if __name__ == "__main__":
    setup_db_for_tests()
