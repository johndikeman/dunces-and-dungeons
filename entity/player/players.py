import base, math, time
import entity.item.weapon as weapons
import dungeon.dungeon as dungeon
import entity.player.player_inventory as inv
import entity.thing as thing
import entity.monster.monsters as monster
import entity.item.consumable as consumable
import entity.ability.player_abilities as ability

RACES = {
	"Tank":{
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
		'abilities':[ability.BattleCry],
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
			'mana': 3.6
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
			'strength': 5,
			'luck': 5,
			'mana': 4
		},
		'LvlGains':{
			'agility': 2,
			'intelligence': 1.6,
			'strength': 1.2,
			'luck': .8,
			'mana': .8
		},
		'abilities':[],
		'statuses':[]
	},
}

class Player(base.Entity):
	def __init__(self,name,test_stats=None): # for test cases
		super(Player,self).__init__()
		self.name = name
		self.party = None
		self.action_points = 2
		self.base_ap = 2
		self.options = ['exit room','examine','dev-examine','map','inventory']
		self.alive = True

		self.health = 0
		self.max_health = 0
		self.armor = 1
		self.gold = 200
		self.equipment = {
			'left':None,
			'right':None,
			'helmet':None,
			'chest':None,
			'legs':None,
			'boots':None,
			'amulet':None,
			'gauntlet':None
		}

		#Please tell me i didn't mess this up.
		if not test_stats:
			option = base.make_choice(RACES.keys(),'race')
			self.race = RACES.keys()[option]
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
			pretty_options = []

			for attribute_set in options:
				# this is an ugly hack to make the string format that i copypasta'd from below work.
				# i have no shame
				self.attributes = attribute_set
				pretty_options.append('%s:%d\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t' % ('agility',self.attributes['agility'],'intelligence',self.attributes['intelligence'],'strength',self.attributes['strength'],'luck',self.attributes['luck'],'mana',self.attributes['mana']))

			ret = base.make_choice(pretty_options,'character setup!')
			#need your help displaying the choices for the player to pick his character.
			self.attributes = options[ret]

			# haha this looks so disgusting
			print self.race +' '+self.name+ '\'s final attributes:\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t%s:%d\n\t' % ('agility',self.attributes['agility'],'intelligence',self.attributes['intelligence'],'strength',self.attributes['strength'],'luck',self.attributes['luck'],'mana',self.attributes['mana'])
		else:
			self.race = test_stats['race']
			self.attributes = test_stats['attributes']

		self.max_health = self.attributes['strength'] * 10
		self.health = self.max_health
		self.inventory.append(consumable.HealthSack())
		self.inventory.append(inv.InventoryHandler())

		# add all the starting abilities
		for a in RACES[self.race]['abilities']:
			self.inventory.append(a())

	def level_up(self):
		for attribute_str in self.attributes.keys():
			self.attributes[attribute_str] += RACES[self.race]['LvlGains'][attribute_str]
			self.max_health=self.attributes['strength'] * 10
			self.health=self.max_health

	def buy_item(self,item):
		if self.gold >= item.get_cost():
			self.gold -= item.get_cost()
			self.inventory.append(item)
			return True
		print "you don't have enough gold for that!"
		return False

	# this method had to be overridden to make armor modifiers work
	def take_damage(self,attacker,damage,wait=True):
		for slot, instance in self.equipment.iteritems():
			if slot is not "left" and slot is not "right":
				if instance:
					instance.register_damage(attacker,damage)
					# print 'did turn on %s' % instance.to_str()
		super(Player,self).take_damage(attacker,damage,wait)

	def return_options(self):
		if not isinstance(self.owner.current_dungeon,dungeon.Hub):
			self.options = ['exit room','examine','map']
			if self.party.current_dungeon.active_room:
				for a in self.party.current_dungeon.active_room.things:
					if isinstance(a,thing.InteractiveObject):
						self.options += a.return_options()
			return super(Player,self).return_options(True)

		else:
			self.options =  ['shop','enter a dungeon','inventory']
			return super(Player,self).return_options(False)

	def do_turn(self, args):
		for x in self.statuses:
			x.do_turn(args)
		# since action points can be removed in the statuses, we need to check it here
		if self.action_points > 0:
			if args == 'save':
				self.party.current_dungeon.save_game()

			if args == 'exit room':
				# door should be the INDEX of the returned list, ie 0 1 2 3
				door = base.make_choice([a for a in self.party.current_dungeon.active_room.get_neighbors().keys()],'room')
				self.party.current_dungeon.active_room.move_to(door)

			## This is the examine method.
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


			# if p == 2:
			# 	print 'you can\'t do that yet, lol'


			if args == 'shop':
				self.party.current_dungeon.enter_shop()


			if args =='map':
				ret = ''
				for x, a in enumerate(self.party.current_dungeon.rooms):
					for y,b in enumerate(a):
						if isinstance(b,dungeon.Room) and self.party.current_dungeon.roomsmap[x][y]=='T':
							ret += 'R '
						elif(isinstance(b,dungeon.Room) and self.party.current_dungeon.roomsmap[x][y]=='?'):
							ret+='? '
						elif(isinstance(b,dungeon.Room) and self.party.current_dungeon.roomsmap[x][y]=='L'):
							ret+='L '
						else:
							ret += '  '
					ret += '\n'
				print ret

			if args == 'enter a dungeon':
				self.party.current_dungeon.leave_dungeon()

			for a in self.inventory:
				if isinstance(a,weapons.Weapon):
					if a.equipped: a.do_turn(args)
				else:
					a.do_turn(args)

		if not isinstance(self.party.current_dungeon,dungeon.Hub):
			for a in self.party.current_dungeon.active_room.things:
				if isinstance(a,thing.InteractiveObject):
					a.do_turn(args)
		self.action_points -= 1

	# IMPORTANT- return value of select_target NEEDS to be validated before use to prevent crashes, cause sometimes it'll return None
	def select_target(self):
		opt = [a for a in self.owner.current_dungeon.active_room.things if(isinstance(a,monster.Monster) and a.revealed)]
		target_ind = base.make_choice([b.to_str() for b in opt],'target')
		if target_ind != None:
			return opt[target_ind]
		return None

	def select_player_target(self):
		opt = base.make_choice([a.to_str() for a in self.party.inventory])
		if opt != None:
			return self.party.inventory[opt]
		return None

	def to_str(self):
		return self.name

	def kill(self,attacker=None):
		pass

	def retaliate(self):
		try:
			if(isinstance(self.equipment['left'],weapons.Weapon) and isinstance(self.equipment['right'],weapons.Weapon)):
				return (self.equipment['left'].damage/3+self.equipment['right'].damage/3)*self.attributes['strength']/4
			elif(isinstance(self.equipment['left'],weapons.Weapon)):
				return (self.equipment['left'].damage/2)*self.attributes['strength']/4
			elif(isinstance(self.equipment['right'],weapons.Weapon)):
				return (self.equipment['right'].damage/2)*self.attributes['strength']/4
			else:
				return self.attributes['strength']/4
		except:
			print "error here, 291 monsters.py"
			return self.attributes['strength']/4

	# this is what items that need to operate in an area of effect need to do.
	# predicate needs to be a function object, which will be called with the entity as the first option
	def do_aoe_monster(self,predicate):
		a = 0
		num=0
		start = len(self.party.current_dungeon.active_room.things)
		for b in self.party.current_dungeon.active_room.things:
			if not isinstance(b,monster.Monster):
				n+=1
		while a < start-num:
			if isinstance(self.party.current_dungeon.active_room.things[a],monster.Monster):
				predicate(self.party.current_dungeon.active_room.things[a])
				if len(self.party.current_dungeon.active_room.things) is start:
					a += 1
				else:
					start = len(self.party.current_dungeon.active_room.things)
	def do_aoe_player(self,predicate):
		a = 0
		start = len(self.party.inventory)
		while a < start:
			predicate(self.party.inventory[a])
			if len(self.party.inventory) is start:
				a += 1
			else:
				start = len(self.party.inventory)


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

	# def get_active(self):
	# 	return self.inventory[self.index]

	def return_options(self):
		return self.inventory[self.index].return_options()

	def get_avg_level(self):
		num = 0
		ind = 0
		for a in self.inventory:
			num += a.level
			ind +=1
		return math.ceil(num/ind)

	def get_active_player(self):
		return self.inventory[self.index]


	def do_turn(self,options):
		self.inventory[self.index].do_turn(options)

	def handle_player_turn(self):
		count=0
		for a in range(len(self.inventory)):
			if(self.inventory[a].alive==False):
				count=count+1
		if(count==len(self.inventory)):
			self.end=False
		for a in range(len(self.inventory)):
			if(self.end):
				print "------====%s's turn====------" % self.inventory[self.index].name
				print 'you have %d hp left' % self.inventory[self.index].health
				while((self.inventory[self.index].action_points > 0) and (self.inventory[self.index].alive==True)):
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
