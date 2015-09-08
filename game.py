from dungeon.dungeon import Dungeon
from entity.player.player import Player, Party

PARTY = []

class Manager:
	def main():
		print "------WELCOME TO DUNCES AND DUNGEONS------"
		party_size = raw_input('enter the size of your party')
		num = 0
		# creating all the players in the party
		for a in range(party_size):
			name = raw_input('enter the name of player %d' % num) 
			PARTY.append(Player(name))
		
		while(True):
			print "it is %s's turn! available options: %s" % ()




if __name__ == '__main__':
	game = Manager()
	game.main()


