from dungeon.dungeon import Dungeon, Hub
from entity.player.players import Player, Party
import entity.item.items as items
import sys

RELEASE_ID = 1

PARTY = Party()
class Manager:
	def main(self):
		# latest = requests.get('https://api.github.com/repos/microwaveabletoaster/dunces-and-dungeons/releases/latest').json()['id']

		# if latest > RELEASE_ID:
		# 	print "---------------===========-----------\nan update to dunces and dungeons has been released! go download it now from here: https://github.com/microwaveabletoaster/dunces-and-dungeons/releases it probably contains super important bugfixes and or more neat features, so don't dawdle!"
		
		print "------WELCOME TO DUNCES AND DUNGEONS------"
		party_size = raw_input('enter the size of your party: ')
		if int(party_size) is 0:
			print "you can't play with zero people, dingus"
			sys.exit()

		# creating all the players in the party
		for a in range(int(party_size)):
			name = raw_input('enter the name of player %d: ' % a) 
			PARTY.add_player(Player(name))
		print 'Game Start'
		print PARTY.to_str()	

		dungeon = Hub(PARTY)

		PARTY.hub = dungeon

		PARTY.current_dungeon = dungeon

		PARTY.current_dungeon.start()

		while(PARTY.end):
			PARTY.handle_player_turn()
			if(PARTY.end):
				PARTY.current_dungeon.handle_monster_turn()
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


