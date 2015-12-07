import base,flask


party = None
app = flask.Flask(__name__)
messages = []
balls = [1,2,3,4,5,6,67,7,8,9,0]

def event_stream():
    while len(messages) > 0:
        d = messages.pop(0)
        for a in d.split('\n'):
            print r'sending %s' % a
            yield 'data: %s\n\n' % a


def run():
    app.debug = False
    app.threaded = True
    app.run()

@app.route('/')
def hello():
    # print messages
    return flask.render_template('main.html')

def put(thing):
    messages.append(thing)
    # print messages

@app.route('/advance',methods=['POST'])
def ad():
    party.handle_player_turn()
    if party.end:
        party.current_dungeon.handle_monster_turn()

@app.route('/stream')
def stream():
    return flask.Response(event_stream(),
                          mimetype="text/event-stream")
