import base, math, time
import entity.item.items as items


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
		self.options = ['leave','examine','dev-examine']
		self.alive = True
		option = base.make_choice(RACES.keys(),'race')
		self.race = RACES.keys()[option]
		self.health = 0
		self.max_health = 0
		choices={}
		self.armor = 0

		#Please tell me i didn't mess this up.

		# options will be the list all the potential dictionarys will be added to
		options = []
		for x in range(3): 
			more_choices={}
			for attribute, dice in RACES[self.race]['rolls'].iteritems():
				rolls = [dice.roll() for a in range(1)]
				selection=0;

				selection = rolls[0]+RACES[self.race]['BaseStats'][attribute]
				# update more choices with the attribute value
				more_choices.update({attribute:selection})
			# when more choices is full, add it to options
			options.append(more_choices)
		# print str(options)

		ret = base.make_choice(options,'character setup!')
		#need your help displaying the choices for the player to pick his character.
		self.attributes = options[ret]

		# haha this looks so disgusting
		print self.race +' '+self.name+ '\'s final attributes:\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t' % ('agility',self.attributes['agility'],'intelligence',self.attributes['intelligence'],'strength',self.attributes['strength'],'luck',self.attributes['luck'],'mana',self.attributes['mana'])
		
		self.max_health = self.attributes['strength'] * 10		
		self.health = self.max_health


		# THIS IS NOT FINAL- ITS A TEST
		self.inventory.append(items.Sword())

	def do_turn(self, args):
		# print args

		for x in self.statuses:
			x.do_turn()

		if args == 'leave':
			# door should be the INDEX of the returned list, ie 0 1 2 3
			door = base.make_choice([a for a in self.party.current_dungeon.active_room.get_neighbors().keys()],'room')
			self.party.current_dungeon.active_room.move_to(door)

		if args == 'examine':
			s = ''
			for ind, a in enumerate(self.party.current_dungeon.active_room.things):
				if ind != len(self.party.current_dungeon.active_room.things) - 1:
					s+='a %s, ' % a.examine(self)
				else:
					s+='and a %s.' % a.examine(self)
			if not s:
				s = 'absolutely nothing.'
			print 'you examine the room and notice %s' % s

		if args == 'dev-examine':
			for a in self.party.current_dungeon.active_room.things:
				print a.dev_examine()



		for a in self.inventory:
			a.do_turn(args)

		self.action_points -= 1

	# IMPORTANT- return value of select_target NEEDS to be validated before use to prevent crashes, cause sometimes it'll return None
	def select_target(self):
		target_ind = base.make_choice([a.to_str() for a in self.owner.current_dungeon.active_room.identified_things],'target')
		if target_ind != None:
			return self.owner.current_dungeon.active_room.identified_things[target_ind]
		return None
		
	def to_str(self):
		return self.name



class Party(base.Entity):
	def __init__(self):
		super(Party,self).__init__()
		self.index = 0
		self.current_dungeon = None
		self.partySize = 0
		self.end=True

	def set_PartySize(self,size):
		self.partySize=size

	def add_player(self,player):
		# party is an entity and all the players will be in
		# the party's inventory
		self.inventory.append(player)
		player.party = self

	def return_options(self):
		return self.inventory[self.index].return_options()


	def do_turn(self,options):
		self.inventory[self.index].do_turn(options)

	def handle_player_turn(self):
		count=0
		for a in range(len(self.inventory)):
			if(self.inventory[self.index].alive==False):
				count=count+1
		if(count==len(self.inventory)):
			self.end=False
		for a in range(len(self.inventory)):
			if(self.end):
				print "------====%s's turn====------" % self.inventory[self.index].name
				while((self.inventory[self.index].action_points > 0) & (self.inventory[self.index].alive==True)):
					selection = base.make_choice(self.return_options(),'option')
					self.do_turn(self.return_options()[selection])

			# set the ap back to start. the subtraction per turn is done in the player do_turn
			self.inventory[self.index].action_points = self.inventory[self.index].base_ap
			self.index += 1

			if self.index == len(self.inventory):
				self.index = 0
	def to_str(self):
		bob=""
		for a in self.inventory:
			bob+= a.race +' '+a.name+ '\'s final attributes:\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t\n' % ('agility',a.attributes['agility'],'intelligence',a.attributes['intelligence'],'strength',a.attributes['strength'],'luck',a.attributes['luck'],'mana',a.attributes['mana'])
		return bob			
