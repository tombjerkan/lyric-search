import flask

from webapp import app


@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')


@app.route('/querysimilarity', methods=['GET', 'POST'])
def query():
    return flask.render_template('querysimilarity.html')
