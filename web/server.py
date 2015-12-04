import flask

class Server(object):
    def __init__(self):
        self.app = flask.Flask(__name__)

    @app.route('/')
    def home(self):
        return flask.render_template('home.html')

    def run(self):
        app.run(debug=True)

    @app.route('/stream')
    def stream(self):
        pass
