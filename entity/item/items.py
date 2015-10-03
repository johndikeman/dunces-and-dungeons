import base,random,math
from misc.words import arcane_words, weapon_words
import entity.status.player_statuses as s
import entity.monster.monsters as r

class Item(base.Entity):
	def __init__(self):
		super(Item,self).__init__()
		self.consumes_inventory_space = True
		# THIS PROBABLY IS NOT FINAL
		self.cost = random.randint(0,10)
		self.name="item"
	def to_str(self):
		return self.name

	def do_turn(self,options):
		pass

class Sword(Item):
	def __init__(self,level):
		super(Sword,self).__init__()
		self.name = 'sword'
		self.level = level
		self.options = ['attack with %s' % self.to_str()]
		self.damage = 10.0 * self.level
		
	def do_turn(self,options):
		# print options
		if self.options[0] in options:
			# print 'swing mah sword'
			target =  self.owner.select_target()
			if target:
				self.swing(target)

	def swing(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['strength'] + base.D12.roll())

class Dagger(Item):
	def __init__(self,level):
		self.name = 'dagger'
		self.level = level
		super(Dagger,self).__init__()
		self.options = ['attack with %s' % self.to_str()]
		self.damage = 5.0 * self.level
		

	def do_turn(self,option):
		if option == self.options[0]:
			target = self.owner.select_target()
			if target:
				self.swing(target)

	def swing(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['strength'] / 2.0 + self.owner.attributes['agility'] / 2.0 + base.D20.roll())

class Bow(Item):
	def __init__(self,level):
		super(Bow,self).__init__()
		self.name='bow'
		self.level = level
		self.options =['Shoot with %s' % self.to_str(), 'Fully draw the %s' % self.to_str()]
		self.damage=7.0 * self.level
	def do_turn(self,option):
		if option == self.options[0]:
			target = self.owner.select_target()
			if target:
				self.shoot(target)

	#an attempt to further increase the action points system. shoot would only cost 1 action point while aim would take 2
	def shoot(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['agility'] + self.owner.attributes['strength'] / 10.0 + base.D12.roll())
	def aim(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['agility'] * 1.8 + self.owner.attributes['strength']/4.0+base.D20.roll())

class Flail(Item):
	def __init__(self,level):
		
		self.level = level
		super(Flail,self).__init__()
		self.name = 'flail'
		self.options = ['attack with %s' % self.to_str()]
		self.damage = 4.0 * self.level

	def do_turn(self,option):
		if option == self.options[0]:
			target = self.owner.select_target()
			if target:
				self.swing(target)

	def swing(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['strength'] / 2.0 + self.owner.attributes['agility'] + self.owner.attributes['luck'] + base.D20.roll())

class Shield(Item):
	def __init__(self,level):
		super(Shield,self).__init__()
		self.name = 'shield'
		self.level = level
		self.options=['Block with %s' % self.to_str(),'Defend Allies with %s' % self.to_str()]
		self.armor=4*self.level
		self.defendin=False
		self.blockin=False 

	#I am not sure how to do the do_turn method.
	def do_turn(self,option):
		if self.defendin:
			for a in self.owner.party.inventory:
				a.armor-=(self.level*2)
			self.defendin=False
		if self.blockin:
			self.owner.armor-=(3*self.level)
			self.blockin=False
		if option == self.options[0]:
			self.block()
		if option == self.options[1]:
			self.defend()
	#Imagining Blocking will increase armor by a set amount on top of the amount given passively from a shield and cost 1 action point
	#while Defending Allies will increase armor of all Allies (including you) by a set amount and cost 2 action points.

	def block(self):
		self.owner.armor+=(3*self.level)
		self.blockin=True

	def defend(self):
		for a in self.owner.party.inventory:
			a.armor+=(2*self.level)
		self.defendin=True
	def apply(self):
		self.owner.armor += self.armor

	def exit(self):
		self.owner.armor -= self.armor


class Breastplate(Item):
	def __init__(self,level):
		super(Breastplate,self).__init__()
		self.name = 'breastplate'
		self.level = level
		self.armor=20
	def apply(self):
		self.owner.armor += self.armor

	def exit(self):
		self.owner.armor -= self.armor

class Chainmail(Item):
	def __init__(self,level):
		super(Chainmail,self).__init__()
		self.name = 'chainmail'
		self.level = level
		self.armor=15
	def apply(self):
		self.owner.armor += self.armor

	def exit(self):
		self.owner.armor -= self.armor

class Platelegs(Item):
	def __init__(self,level):
		super(Platelegs,self).__init__()
		self.name = 'platelegs'
		self.level = level
		self.armor=12
	def apply(self):
		self.owner.armor += self.armor

	def exit(self):
		self.owner.armor -= self.armor

class Helmet(Item):
	def __init__(self,level):
		super(Helmet,self).__init__()
		self.name = 'helmet'
		self.level = level
		self.armor=13
	def apply(self):
		self.owner.armor += self.armor

	def exit(self):
		self.owner.armor -= self.armor

class SpellBook(Item):
	def __init__(self,level):
		super(SpellBook,self).__init__()
		self.cost = random.randint(0,10)
		self.level = level
		self.name = ''
		# hahahahahaha this is so fucking stupid
		level = int(math.ceil(level))
		for a in range(int(math.ceil(level))):
			self.name += " %s" % random.choice(arcane_words)
		self.options = ['cast %s' % self.name,'rename %s' % self.name,'examine %s' % self.name]
		self.stuntime = random.choice(range(level * 4))
		self.poisontime = random.choice(range(level * 4))
		self.damage = random.choice(range(-20*level,20*level))
		self.poisondamage = random.choice(range(-5*level,5*level))
		self.aoe = random.choice([True,False])
		self.on_cooldown = False
		self.cooldown_time = random.choice(range(4*level,7*level))

	def do_turn(self,option):
		# effectiveness coefficient
		ec = self.owner.attributes['mana'] / 5
		if option == self.options[1]:
			name = raw_input('enter a new name for %s' % self.name)
			self.name = name

		if option == self.options[2]:
			print self.descr()

		if option == self.options[0]:
			if not self.on_cooldown:
				if not self.aoe:
					targets = [self.owner.select_target()]
				else:
					targets = self.owner.party.current_dungeon.active_room.things
				for target in targets:
					if target:
						if self.damage:
							target.take_damage(self.owner,self.damage*ec)
						if self.stuntime:
							target.statuses.append(s.Stun(math.ceil(self.stuntime*ec)))
						if self.poisontime and self.poisondamage:
							target.statuses.append(s.Poison(math.ceil(self.poisontime*ec),self.poisondamage*ec))
				self.owner.statuses.append(s.Cooldown(self,self.cooldown_time))
			else:
				print '%s is on cooldown!' % self.name

		self.options = ['cast %s' % self.name,'rename %s' % self.name,'examine %s' % self.name]

	def to_str(self):
		return 'a spell by the name of %s' % self.name

	def descr(self):
		ret =  "%s does %.2f damage, stuns for %d turns and does %.2f of poison damage every turn for %d turns " % (self.name,self.damage,self.stuntime,self.poisondamage,self.poisontime)
		if self.aoe:
			ret += 'in an area of effect.'
		else:
			ret += 'to a single target.'
		return ret		


class ItemController():
	def __init__(self,party):
		self.items = {
			'weapons':[Sword,Dagger,Bow,Flail],
			'armor':[Shield,Breastplate,Chainmail,Platelegs,Helmet],
			'spells':[SpellBook]
		}
		self.party = party
		self.applier = r.Apply()

	def generate(self,kind):
		if kind == 'weapons':
			return self.get_weapon()
		elif kind == 'armor':
			return self.get_armor()
		elif kind == 'spells':
			return self.get_spells()
		else:
			return None

	def get_weapon(self):
		weapon_instance = self.applier.modify_item(random.choice(self.items['weapons'])(self.party.get_avg_level()))
		# if base.D12.roll() > 9:
		# 	word = random.choice(words.weapon_words)
		# 	weapon_instance.name = '%s %s' % (word, weapon_instance.name)
		# 	if word == 'sharp':
		# 		weapon_instance.damage *= 1.3
		# 	if word == 'quick':
		# 		weapon_instance.damage *= 1.5
		# 	if word == 
		# else:
		return weapon_instance

	def get_armor(self):
		armor_instance = random.choice(self.items['armor'])(self.party.get_avg_level())
		return armor_instance

	def get_spells(self):
		spell_instance = SpellBook(self.party.get_avg_level())
		return spell_instance

