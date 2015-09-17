import base

RACES = {
	"Dwarf":{
		"rolls":{
			'agility': base.D6,
			'intelligence':base.D12,
			'strength':base.D20,
			'luck':base.D6,
			'mana':base.D2
		},
		'BaseStats':{
			'agility': 2,
			'intelligence': 5,
			'strength': 8,
			'luck': 3,
			'mana': 0
		},
		'LvlGains':{
			'agility': 1.4,
			'intelligence': 2,
			'strength': 3.6,
			'luck': 1,
			'mana': .2
		},
		'abilities':[],
		'statuses':[]
	},
	'Wizard':{
		"rolls":{
			'agility': base.D12,
			'intelligence':base.D20,
			'strength':base.D6,
			'luck':base.D6,
			'mana':base.D12
		},
		'BaseStats':{
			'agility': 4,
			'intelligence': 9,
			'strength': 2,
			'luck': 3,
			'mana': 4
		},
		'LvlGains':{
			'agility': 2,
			'intelligence': 4,
			'strength': 1,
			'luck': 1,
			'mana':1.6
		},
		'abilities':[],
		'statuses':[]
	},
	'Ranger':{
		"rolls":{
			'agility': base.D20,
			'intelligence':base.D12,
			'strength':base.D12,
			'luck':base.D6,
			'mana':base.D6
		},
		'BaseStats':{
			'agility': 6,
			'intelligence': 3,
			'strength': 4,
			'luck': 3,
			'mana': 2
		},
		'LvlGains':{
			'agility': 3.2,
			'intelligence': 1.8,
			'strength': 2.2,
			'luck': 1,
			'mana': .8
		},
		'abilities':[],
		'statuses':[]
	},
	'Rogue':{
		"rolls":{
			'agility': base.D20,
			'intelligence':base.D12,
			'strength':base.D20,
			'luck':base.D6,
			'mana':base.D6
		},
		'BaseStats':{
			'agility': 8,
			'intelligence': 6,
			'strength': 9,
			'luck': 5,
			'mana': 4
		},
		'LvlGains':{
			'agility': 2,
			'intelligence': 1.6,
			'strength': 2.2,
			'luck': .8,
			'mana': .8
		},
		'abilities':[],
		'statuses':[]
	},
}

class Player(base.Entity):
	def __init__(self,name):
		super(Player,self).__init__()
		self.name = name
		self.party = None
		self.action_points = 2
		self.options = ['leave']
		self.alive = True
		option = base.make_choice(RACES.keys(),'race')
		self.race = RACES.keys()[option]
		self.health = 0
		self.max_health = 0
		choices={}

		#Please tell me i didn't mess this up.

		# options will be the list all the potential dictionarys will be added to
		options = []
		for x in range(3): 
			more_choices={}
			for attribute, dice in RACES[self.race]['rolls'].iteritems():
				rolls = [dice.roll() for a in range(3)]
				selection=0;

				# find the largest roll out of three
				for b in range(3):
					if rolls[b] > selection:
						selection = rolls[b]+RACES[self.race]['BaseStats'][attribute]
				# update more choices with the attribute value
				more_choices.update({attribute:selection})
			# when more choices is full, add it to options
			options.append(more_choices)
		# print str(options)

		ret = base.make_choice(options,'character setup!')
		#need your help displaying the choices for the player to pick his character.
		self.attributes = options[ret]

		# haha this looks so disgusting
		print 'final attributes:\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t' % ('agility',self.attributes['agility'],'intelligence',self.attributes['intelligence'],'strength',self.attributes['strength'],'luck',self.attributes['luck'],'mana',self.attributes['mana'])
		
		self.max_health = self.attributes['strength'] * 10		
		self.health = self.max_health


	def do_turn(self, args):
		# print args

		for x in self.statuses:
			x.do_turn()

		if 'leave' in args:
			# door should be the INDEX of the returned list, ie 0 1 2 3
			door = raw_input('choose a door to exit from. (0-%s)' % str(len(self.party.current_dungeon.active_room.neighbors)-1))
			self.party.current_dungeon.active_room.move_to(int(door))

		for a in self.inventory:
			a.do_turn(args)

	def take_damage(self,damage):
		pass




class Party(base.Entity):
	def __init__(self):
		super(Party,self).__init__()
		self.index = 0
		self.current_dungeon = None

	def add_player(self,player):
		# party is an entity and all the players will be in
		# the party's inventory
		self.inventory.append(player)
		player.party = self

	def return_options(self):
		print "it is %s's turn!" % self.inventory[self.index].name
		print 'options: %s' % str(self.inventory[self.index].return_options())


	def do_turn(self,options):
		self.inventory[self.index].do_turn(options)
		self.inventory[self.index].action_points -= 1

	def handle_player_turn(self):
		while(self.inventory[self.index].action_points > 0):
			self.return_options()
			self.do_turn(raw_input().split(' '))
		self.inventory[self.index].action_points = self.inventory[self.index].base_ap
		self.index += 1

		if self.index == len(self.inventory):
			self.index = 0

