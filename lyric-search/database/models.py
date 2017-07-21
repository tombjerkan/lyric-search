import numpy
import sqlalchemy
import sqlalchemy.ext.declarative


Base = sqlalchemy.ext.declarative.declarative_base()


class Song(Base):
    __tablename__ = 'Song'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(100))
    artist = sqlalchemy.Column(sqlalchemy.String(100))
    lyrics = sqlalchemy.Column(sqlalchemy.String(2000))
