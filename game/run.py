from dungeon.dungeon import Dungeon
from entity.player.players import Player, Party

PARTY = []

class Manager:
	def main(self):
		print "------WELCOME TO DUNCES AND DUNGEONS------"
		party_size = raw_input('enter the size of your party')
		num = 0
		# creating all the players in the party
		for a in range(int(party_size)):
			name = raw_input('enter the name of player %d' % num) 
			PARTY.append(Player(name))
			num += 1
			if num == int(party_size):
				num = 0

		while(True):
			options =  raw_input("it is %d's turn! available options: %s" % (num,str(PARTY[num].return_options())))
			PARTY[num].process_options(options.split(" "))

		return 0




if __name__ == '__main__':
	game = Manager()
	game.main()


