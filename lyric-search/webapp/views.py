import flask

from webapp import app
from .forms import QueryForm


@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')


@app.route('/querysimilarity', methods=['GET', 'POST'])
def query():
    form = QueryForm()
    return flask.render_template('querysimilarity.html', form=form)
