import contextlib
import sqlalchemy

from . import models

from configobj import ConfigObj
_config = ConfigObj('settings.cfg')


def create_database():
    engine = sqlalchemy.create_engine(_config['DB_CONNECTION_STRING'])
    models.Base.metadata.create_all(engine)


@contextlib.contextmanager
def session_scope():
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
