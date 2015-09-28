from dungeon.dungeon import Dungeon, Hub
from entity.player.players import Player, Party
import entity.item.items as items

PARTY = Party()
class Manager:
	def main(self):
		print "------WELCOME TO DUNCES AND DUNGEONS------"
		party_size = raw_input('enter the size of your party: ')

		# creating all the players in the party
		for a in range(int(party_size)):
			name = raw_input('enter the name of player %d: ' % a) 
			PARTY.add_player(Player(name))
		print 'Game Start'
		print PARTY.to_str()	

		dungeon = Hub(PARTY)

		PARTY.current_dungeon = dungeon

		dungeon.start()

		while(PARTY.end):
			PARTY.handle_player_turn()
			if(PARTY.end):
				dungeon.handle_monster_turn()
		print "              "
		print "              "
		print "              "
		print "              "
		print "              "
		print "              "
		print "              "
		print "              "
		print "              "
		print "              "
		print "                 *****GAME OVER*****"



if __name__ == '__main__':
	game = Manager()
	game.main()


