from flask_wtf import FlaskForm
from wtforms import StringField


class QueryForm(FlaskForm):
    query = StringField('query')


class SongForm(FlaskForm):
    song_title = StringField('song_title')
    artist = StringField('artist')
