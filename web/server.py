import flask,threading,Queue,time
# from dungeon.dungeon import Dungeon, Hub
# from entity.player.players import Player, Party
# import entity.item.items as items
# the redis thing
from data import r

party = None
app = flask.Flask(__name__)
messages = []
choice_results = []
r.delete('out')
r.delete('in')
r.delete('cache')

# pubsub = r.pubsub()


def event_stream():
    # pubsub.subscribe('out')
    for d in r.lrange('out',0,-1)[::-1]:
        print d
        for a in r.rpoplpush('out','cache').split('\n'):
            print r'sending %s' % a
            yield 'data: %s\n\n' % a
        # break
    # pubsub.unsubscribe()
    # print 'here'

def run():
    app.debug = True
    app.threaded = True
    app.run()


@app.route('/')
def hello():
    # print messages
    return flask.render_template('main.html',db=r)

def put(thing):
    messages.append(thing)
    # print messages

@app.route('/advance',methods=['POST'])
def ad():
    return flask.redirect('/')

@app.route('/choice',methods=['POST'])
def ch():
    r.publish('in',flask.request.form['makechoice'])
    print flask.request.form['makechoice']
    return flask.redirect('/')

@app.route('/stream')
def stream():
    return flask.Response(event_stream(),
                          mimetype="text/event-stream")


if __name__ == '__main__':
    run()
