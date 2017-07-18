import contextlib
import sqlalchemy

from . import models


def create_database(database_file):
    engine = sqlalchemy.create_engine(database_file)
    models.Base.metadata.create_all(engine)


@contextlib.contextmanager
def session_scope(database_file):
    engine = sqlalchemy.create_engine(database_file)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
