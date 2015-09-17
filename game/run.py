from dungeon.dungeon import Dungeon
from entity.player.players import Player, Party

PARTY = Party()
class Manager:
	def main(self):
		print "------WELCOME TO DUNCES AND DUNGEONS------"
		party_size = raw_input('enter the size of your party: ')

		# creating all the players in the party
		for a in range(int(party_size)):
			name = raw_input('enter the name of player %d: ' % a) 
			PARTY.add_player(Player(name))

		dungeon = Dungeon(12,1,PARTY)

		PARTY.current_dungeon = dungeon

		dungeon.start()

		while(True):
			PARTY.handle_player_turn()



if __name__ == '__main__':
	game = Manager()
	game.main()


