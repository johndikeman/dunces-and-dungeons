import base
class Player(base.Entity):
	def __init__(self,name):
		super(Player,self).__init__()
		self.name = name
		self.party = None

	def process_options(self,*args):
		for a in self.inventory.keys():
			self.inventory[a].process_options(args)




class Party(base.Entity):
	def __init__(self):
		super(Party,self).__init__()
		self.index = 0

	def add_player(self,player):
		# party is an entity and all the players will be in
		# the party's inventory
		self.inventory.append(player)
		player.party = self

	def return_options(self):
		print "it is %s's turn!" % self.inventory[self.index].name
		print 'options: %s' % str(self.inventory[self.index].return_options())


	def do_turn(self,*options):
		self.inventory[self.index].do_turn(options)
		self.inventory[self.index].action_points -= 1

	def handle_player_turn(self):
		while(self.inventory[self.index].action_points > 0):
			self.return_options()
			self.do_turn(raw_input())
		self.inventory[self.index].action_points = self.inventory[self.index].base_ap
		self.index += 1

		if self.index == len(self.inventory):
			self.index = 0
