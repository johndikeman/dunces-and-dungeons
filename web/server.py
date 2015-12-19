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
r.delete('choiceskip')
r.set('choiceskip',0)

# pubsub = r.pubsub()

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
    thing = flask.request.form['makechoice'].split('%')
    print thing

    r.publish('in',thing[1]) # the zero value of this split should  be the exact query
    # remove the choice from the database when we get a value from it
    r.incr('choiceskip',1)
    return flask.redirect('/')

@app.route('/positioning',methods=['POST'])
def pos():
    flask.request.get_data()
    r.set('positions',flask.request.data)

@app.route('/input',methods=['POST'])
def i():
    val = thing = flask.request.form['input']
    r.publish('in',val)
    r.incr('choiceskip',1)
    return flask.redirect('/')

if __name__ == '__main__':
    run()
