import base,flask,threading,Queue,time
from dungeon.dungeon import Dungeon, Hub
from entity.player.players import Player, Party
import entity.item.items as items


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
    ghghg()


def ghghg():
    app.debug = False
    app.threaded = True
    app.run()
    th = threading.Thread(target=newgame)
    th.start()


def newgame():
    PARTY = Party()
    party_size = base.get_input('enter the size of your party: ')
    if int(party_size) is 0:
        base.put("you can't play with zero people, dingus")
        sys.exit()
    # creating all the players in the party
    for a in range(int(party_size)):
        name = base.get_input('enter the name of player %d: ' % a)
        PARTY.add_player(Player(name))
    base.put('Game Start')
    base.put(PARTY.to_str())
    dungeon = Hub(PARTY)
    PARTY.hub = dungeon
    PARTY.current_dungeon = dungeon
    PARTY.current_dungeon.start()

@app.route('/')
def hello():
    # print messages
    return flask.render_template('main.html',party=party)

def put(thing):
    messages.append(thing)
    # print messages

@app.route('/advance',methods=['POST'])
def ad():
    th = threading.Thread(target=plsgod)
    th.start()

def plsgod():
    party.handle_player_turn()

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
