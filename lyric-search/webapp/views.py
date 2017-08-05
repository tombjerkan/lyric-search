import flask

from lyricprocessor.similarity import similarity_to_query
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
    return flask.render_template('songsimilarity.html', form=form)
