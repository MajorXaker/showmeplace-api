from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, as_declarative

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

#
@as_declarative(metadata=MetaData(naming_convention=convention))
class Model:
    metadata: MetaData


# Model = declarative_base(metadata=MetaData(naming_convention=convention))

# db = create_engine("postgresql+psycopg2://mastermind:master_hrinder@localhost/hrinder")
