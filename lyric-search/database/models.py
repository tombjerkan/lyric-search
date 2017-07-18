import sqlalchemy
import sqlalchemy.ext.declarative


Base = sqlalchemy.ext.declarative.declarative_base()


class Song(Base):
    __tablename__ = 'Song'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(100))
    artist = sqlalchemy.Column(sqlalchemy.String(100))
    lyrics = sqlalchemy.Column(sqlalchemy.String(2000))

    vector = sqlalchemy.orm.relationship(
        'VectorFeature',
        order_by=lambda: VectorFeature.feature_index
    )


class VectorFeature(Base):
    __tablename__ = 'VectorFeature'

    song_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('Song.id'),
        primary_key=True
    )

    feature_index = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    feature_value = sqlalchemy.Column(sqlalchemy.Float)
