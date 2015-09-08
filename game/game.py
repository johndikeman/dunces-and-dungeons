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
			num += 1
			if num == party_size:
				num = 0

		while(True):
			options =  raw_input("it is %d's turn! available options: %s" % (num,str(PARTY[num].return_options())))
			PARTY[num].process_options(options.split(" "))




if __name__ == '__main__':
	game = Manager()
	game.main()


