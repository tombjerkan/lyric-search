import contextlib
import sqlalchemy

from . import models

from configobj import ConfigObj
_config = ConfigObj('settings.cfg')


_engine = sqlalchemy.create_engine(_config['DB_CONNECTION_STRING'])
_session_factory = sqlalchemy.orm.sessionmaker(bind=_engine)
_Session = sqlalchemy.orm.scoped_session(_session_factory)


def create_database():
    """Creates the database and its tables."""
    models.Base.metadata.create_all(_engine)


@contextlib.contextmanager
def session_scope():
    """Returns a session context for the database.

    Committing, rollbacks and closing for the session is handled automatically
    by the context manager.
    """
    session = _Session()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
