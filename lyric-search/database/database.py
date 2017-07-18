import sqlalchemy

from . import models


def create_database(database_file):
    engine = sqlalchemy.create_engine(database_file)
    models.Base.metadata.create_all(engine)
