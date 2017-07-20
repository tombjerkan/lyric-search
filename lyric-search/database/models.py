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

    _vector = sqlalchemy.orm.relationship(
        'VectorFeature',
        order_by=lambda: VectorFeature.index
    )

    @property
    def vector(self):
        return [(numpy.int64(feature.index), numpy.float64(feature.value))
                for feature in self._vector]


class VectorFeature(Base):
    __tablename__ = 'VectorFeature'

    song_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('Song.id'),
        primary_key=True
    )

    index = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    value = sqlalchemy.Column(sqlalchemy.Float)
