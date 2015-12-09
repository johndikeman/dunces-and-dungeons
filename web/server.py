import base,flask,threading,Queue,time


party = None
app = flask.Flask(__name__)
messages = []
balls = [1,2,3,4,5,6,67,7,8,9,0]
choice_results = []

def event_stream():
    while len(messages) > 0:
        d = messages.pop(0)
        for a in d.split('\n'):
            print r'sending %s' % a
            yield 'data: %s\n\n' % a

def run():
    th = threading.Thread(target=ghghg)
    th.start()


def ghghg():
    app.debug = False
    app.threaded = True
    app.run()

@app.route('/')
def hello():
    # print messages
    return flask.render_template('main.html',party=party)

def put(thing):
    messages.append(thing)
    # print messages

@app.route('/advance',methods=['POST'])
def ad():
    return flask.redirect('/da')

@app.route('/choice')
def ch():
    choice_results.append(flask.request.value)
    print flask.request.value

def ra():
    while len(choice_results) == 0:
        pass
    return choice_results.pop(0)

@app.route('/stream')
def stream():
    return flask.Response(event_stream(),
                          mimetype="text/event-stream")
