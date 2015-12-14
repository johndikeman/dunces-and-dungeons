import base, math, time
import entity.item.weapon as weapons
import dungeon.dungeon as dungeon
import entity.player.player_inventory as inv
import entity.thing as thing
import entity.monster.monsters as monster
import entity.item.consumable as consumable
import entity.ability.player_abilities as ability
import entity.item.utils as utils
import os

try:
	import dill
except:
	dill = None

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
			'agility': 10,
			'intelligence': 10,
			'strength': 30,
			'luck': 7,
			'mana': 0
		},
		'LvlGains':{
			'agility': 1.4,
			'intelligence': 2,
			'strength': 6,
			'luck': 1,
			'mana': .2
		},
		'abilities':[ability.BattleCry, ability.BerserkerVitality],
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
			'agility': 5,
			'intelligence': 25,
			'strength': 10,
			'luck': 8,
			'mana': 30
		},
		'LvlGains':{
			'agility': 2,
			'intelligence': 4,
			'strength': 1.4,
			'luck': 1,
			'mana': 6
		},
		'abilities':[ability.Forget,ability.Dementia],
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
			'agility': 12,
			'intelligence': 12,
			'strength': 12,
			'luck': 12,
			'mana': 12
		},
		'LvlGains':{
			'agility': 4.6,
			'intelligence': 2.4,
			'strength': 3.8,
			'luck': 1.5,
			'mana': 1.2
		},
		'abilities':[ability.Perseverance, ability.Swap],
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
			'agility': 30,
			'intelligence': 30,
			'strength': 40,
			'luck': 14,
			'mana': 18
		},
		'LvlGains':{
			'agility': 2.4,
			'intelligence': 1.6,
			'strength': 2.4,
			'luck': 1.2,
			'mana': .6
		},
		'abilities':[ability.Steal, ability.Quickness],
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
		self.options = ['exit room','examine','dev-examine','inventory']
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
		# self.inventory.append(utils.Map())

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
			self.options = ['exit room','examine']
			if self.party.current_dungeon.active_room:
				for a in self.party.current_dungeon.active_room.things:
					if isinstance(a,thing.InteractiveObject):
						self.options += a.return_options()
			return super(Player,self).return_options(True)

		else:
			self.options =  ['shop','enter a dungeon','inventory','save','load']
			return super(Player,self).return_options(False)

	def do_turn(self):
		for x in self.statuses:
			x.do_turn(None)

		# since action points can be removed in the statuses, we need to check it here
		if self.action_points > 0:
			args = self.return_options()[base.make_choice(self.return_options())]
			if args == 'save':
				if dill:
					name = raw_input('enter the name of your save: ')
					if not os.path.exists('%s/saves/' % base.BASE_DIR):
						os.makedirs('%s/saves/' % base.BASE_DIR)

					path = '%s/saves/%s.dunce' % (base.BASE_DIR,name)
					# have to create the file before we take a dump in it
					with open(path,'w+'):
						pass
					dill.dump_session(path)

			if args == 'load':
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
						self.action_points = 0
						dill.load_session('%s/saves/%s' % (base.BASE_DIR,li[op]))
				else:
					print 'save/load support is disabled because you haven\'t installed dill!'


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

	def get_healthbar(self,size=12):
		bar = '['
		num = int(math.floor(self.health / (self.max_health / (size * 1.0))))
		rest = size - num
		for a in range(num):
			bar += '='
		for a in range(rest):
			bar += ' '
		return bar + ']'

	def get_xpbar(self,size=12):
		bar = '['
		num = int(math.floor(self.xp / ((self.level_up_threshold + 1) / (size * 1.0))))
		rest = size - num
		for a in range(num):
			bar += '='
		for a in range(rest):
			bar += ' '
		return bar + ']'


	def select_player_target(self):
		opt = base.make_choice([a.to_str() for a in self.party.inventory])
		if opt != None:
			return self.party.inventory[opt]
		return None

	def to_str(self):
		return self.name

	def kill(self,attacker=None):
		pass

	def retaliate(self,target):
		try:
			if(isinstance(self.equipment['left'],weapons.Weapon) and isinstance(self.equipment['right'],weapons.Weapon)):
				return (self.equipment['left'].standard_attack(target)/10+self.equipment['right'].standard_attack(target)/10)
			elif(isinstance(self.equipment['left'],weapons.Weapon)):
				return (self.equipment['left'].standard_attack(target)/7)
			elif(isinstance(self.equipment['right'],weapons.Weapon)):
				return (self.equipment['right'].standard_attack(target)/7)
			else:
				return self.attributes['strength']/4
		except:
			print "error here, 358 players.py"
			return self.attributes['strength']/4

	# this is what items that need to operate in an area of effect need to do.
	# predicate needs to be a function object, which will be called with the entity as the first option
	def do_aoe_monster(self,predicate):
		b = len(self.party.current_dungeon.active_room.things)
		a = 0
		while a < b:
			if isinstance(self.party.current_dungeon.active_room.things[a],monster.Monster):
				firstr=self.party.current_dungeon.active_room.things[a].alive
				work=self.party.current_dungeon.active_room.things[a]
				predicate(self.party.current_dungeon.active_room.things[a])
				try:
					if firstr and not work.alive:
						a -= 1
						b -= 1
				except:
					a -= 1
					b -= 1
			a+=1
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


	def do_turn(self):
		self.inventory[self.index].do_turn()

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
				print 'HEALTH: %s' % self.inventory[self.index].get_healthbar(24)
				print 'XP: %s' % self.inventory[self.index].get_xpbar(24)
				while((self.inventory[self.index].action_points > 0) and (self.inventory[self.index].alive==True)):
					self.do_turn()

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
