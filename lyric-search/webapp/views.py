import flask

from database.tools import session_scope
from database.models import Song
from lyricprocessor.similarity import similarity_to_query, similarity_to_song
from webapp import app
from .forms import QueryForm, SongForm


@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')


@app.route('/querysimilarity', methods=['GET', 'POST'])
def query():
    form = QueryForm()

    if form.validate_on_submit():
        similar_songs = similarity_to_query(form.query.data)
        return flask.render_template(
            'querysimilarity.html',
            form=form,
            songs=similar_songs
        )
    else:
        return flask.render_template('querysimilarity.html', form=form)


@app.route('/songsimilarity', methods=['GET', 'POST'])
def song():
    form = SongForm()

    if form.validate_on_submit():
        with session_scope() as session:
            song_query = session.query(Song)
            song_query = song_query.filter(Song.title == form.song_title.data)
            song_query = song_query.filter(Song.artist == form.artist.data)
            song = song_query.first()

        similar_songs = similarity_to_song(song)
        return flask.render_template(
            'songsimilarity.html',
            form=form,
            songs=similar_songs
        )
    else:
        return flask.render_template('songsimilarity.html', form=form)
