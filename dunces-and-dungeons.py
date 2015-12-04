from dungeon.dungeon import Dungeon, Hub
from entity.player.players import Player, Party
import entity.item.items as items
import sys, os
import base

try:
	import dill
except:
	dill = None


PARTY = Party()
class Manager:
	def __init__(self):
		self.checked = False

	def get_current_release(self):
		latest = None
		try:
			import requests
			latest = requests.get('https://api.github.com/repos/microwaveabletoaster/dunces-and-dungeons/releases/latest').json()['tag_name']
		except:
			print "could not reach the update service :'("
		return latest

	def update_check(self):
		print 'checking for update...'
		latest = self.get_current_release()

		if latest:
			if latest == self.RELEASE_ID:
				print 'you\'re up to date!'
			else:
				print "---------------=====UPDATE!!=====-----------\nan update to dunces and dungeons has been released! \ngo download it now from here: https://github.com/microwaveabletoaster/dunces-and-dungeons/releases \nit probably contains super important bugfixes and or more neat features, so don't dawdle!! \n\n<3 the team\n"
		self.checked = True

	def main(self):
		base.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		ver = []
		with open('%s/version.dunce' % base.BASE_DIR, 'r+') as f:
			contents = f.read()
			ver = contents.split(' ')
		self.RELEASE_ID = ('v%s.%s.%s' % (ver[0],ver[1],ver[2])).strip()

		if not self.checked:
			self.update_check()
		go = True
		print "------=====WELCOME TO DUNCES AND DUNGEONS=====------"
		cho = 0

		if cho is not None:
			if cho is 0:
				self.new_game()
			if cho is 1:
				li = []
				if os.path.exists('%s/saves/' % base.BASE_DIR):
					for dirpath, dirname, filename in os.walk('%s/saves/' % base.BASE_DIR):
						for fi in filename:
							if '.dunce' in fi:
								li.append(fi)
				else:
					print 'no saves to choose from!'
				op = base.make_choice(li,"savefile")
				if dill:
					if op is not None:
						go = False
						print 'loading session'
						dill.load_session('%s/saves/%s' % (base.BASE_DIR,li[op]))
				else:
					print 'save/load support is disabled because you haven\'t installed dill!'

	def new_game(self):
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
		print "\n\n------------=========GAME OVER=========------------"


if __name__ == '__main__':
	game = Manager()
	game.main()
