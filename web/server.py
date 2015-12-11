import flask,threading,Queue,time
# from dungeon.dungeon import Dungeon, Hub
# from entity.player.players import Player, Party
# import entity.item.items as items
# the redis thing
from data import r


party = None
app = flask.Flask(__name__)
messages = []
balls = [1,2,3,4,5,6,67,7,8,9,0]
choice_results = []

# pubsub = r.pubsub()


def event_stream():
    # pubsub.subscribe('out')
    for d in r.lrange('out',0,-1):
        for a in r.rpop('out').split('\n'):
            print r'sending %s' % a
            yield 'data: %s\n\n' % a
        # break
    # pubsub.unsubscribe()
    print 'here'

def run():
    app.debug = True
    app.threaded = True
    app.run()
    # print 'print here'
    # th = threading.Thread(target=newgame)
    # th.start()


# def newgame():
#     print 'newgame called'
#     PARTY = Party()
#     party_size = base.get_input('enter the size of your party: ')
#     if int(party_size) is 0:
#         base.put("you can't play with zero people, dingus")
#         sys.exit()
#     # creating all the players in the party
#     for a in range(int(party_size)):
#         name = base.get_input('enter the name of player %d: ' % a)
#         PARTY.add_player(Player(name))
#     base.put('Game Start')
#     base.put(PARTY.to_str())
#     dungeon = Hub(PARTY)
#     PARTY.hub = dungeon
#     PARTY.current_dungeon = dungeon
#     PARTY.current_dungeon.start()

@app.route('/')
def hello():
    # print messages
    return flask.render_template('main.html',party=party)

def put(thing):
    messages.append(thing)
    # print messages

@app.route('/advance',methods=['POST'])
def ad():
    pass

@app.route('/choice',methods=['POST'])
def ch():
    r.publish('in',flask.request.value)
    print flask.request.value

@app.route('/stream')
def stream():
    return flask.Response(event_stream(),
                          mimetype="text/event-stream")


if __name__ == '__main__':
    run()
