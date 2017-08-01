import contextlib
import sqlalchemy

from . import models

from configobj import ConfigObj
_config = ConfigObj('settings.cfg')


def create_database():
    """Creates the database and its tables.

    The database is created according to the DB_CONNECTION_STRING config
    setting.
    """
    engine = sqlalchemy.create_engine(_config['DB_CONNECTION_STRING'])
    models.Base.metadata.create_all(engine)


@contextlib.contextmanager
def session_scope():
    """Returns a session context for the database.

    Returns a session context for the database given by the
    DB_CONNECTION_STRING config setting.

    Committing, rollbacks and closing for the session is handled automatically
    by the context manager.
    """
    engine = sqlalchemy.create_engine(_config['DB_CONNECTION_STRING'])
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
