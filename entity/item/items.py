import base,random,math
from misc.words import arcane_words, weapon_words
import entity.status.player_statuses as s
import entity.monster.monsters as r


class Item(base.Entity):
	def __init__(self):
		super(Item,self).__init__()
		self.consumes_inventory_space = True
		# THIS PROBABLY IS NOT FINAL
		self.cost = 5
		self.name="item"
		self.equipped = False

	def to_str(self):
		return self.name

	def do_turn(self,options):
		pass

	def return_options(self):
		if self.equipped:
			return super(Item,self).return_options()
		return []

	def equip(self):
		if self.info == 'one-handed':
			# this gets the name of the item in both hands, to let the player
			# know what they are going to equip
			if self.owner.equipment['left']:
				left = self.owner.equipment['left'].to_str()
			else:
				left = 'Nothing'

			if self.owner.equipment['right']:
				right = self.owner.equipment['right'].to_str()
			else:
				right = 'Nothing'

			side=base.make_choice(['left (%s)' % left,'right (%s)' % right])
			try:
				self.owner.equipment[['left','right'][side]].unequip()
			except:
				pass
			self.owner.equipment[['left','right'][side]] = self
		elif self.info =='two-handed':
			try:
				self.owner.equipment['left'].unequip()
			except:
				try:
					self.owner.equipment['right'].unequip()
				except:
					pass
			self.owner.equipment['left']=self
			self.owner.equipment['right']=self
		elif self.owner.equipment[self.info]:
			self.owner.equipment[self.info].unequip()
			self.owner.equipment[self.info] = self
		self.equipped = True

	def unequip(self):
		self.equipped = False

	def examine(self):
		try:
			return self.descr
		except:
			return 'a %s' % self.to_str()

	def get_cost(self):
		return self.cost


class Weapon(Item):
	def __init__(self):
		super(Weapon,self).__init__()

	def get_cost(self):
		return self.damage * self.cost

class Sword(Weapon):
	def __init__(self,level):
		super(Sword,self).__init__()
		self.name = 'sword'
		self.info='one-handed'
		self.info2='weapon'
		self.level = level
		self.options = ['%s' % self.to_str()]
		self.item_options=['examine','equip']
		self.damage = 10.0 * self.level
		self.cost = 10

	def do_turn(self,options):
		self.options = ['%s' % self.to_str()]
		# print options
		if self.options[0] in options:
			p = base.make_choice(['swing %s' % self.to_str()])
			if p == 0:
				target = self.owner.select_target()
				if target:
					self.swing(target)

	def swing(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['strength'] + base.D12.roll())

class Dagger(Weapon):
	def __init__(self,level):
		super(Dagger,self).__init__()
		self.name = 'dagger'
		self.level = level
		self.info='one-handed'
		self.info2='weapon'
		self.item_options=['examine','equip']
		self.options = ['%s' % self.to_str()]
		self.damage = 5.0 * self.level


	def do_turn(self,option):
		self.options = ['%s' % self.to_str()]

		if option == self.options[0]:
			p = base.make_choice(['attack with %s'])
			if p == 0:
				target = self.owner.select_target()
				if target:
					self.swing(target)

	def swing(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['strength'] / 2.0 + self.owner.attributes['agility'] / 2.0 + base.D20.roll())

class Bow(Weapon):
	def __init__(self,level):
		super(Bow,self).__init__()
		self.name='bow'
		self.info='two-handed'
		self.info2='weapon'
		self.level = level
		self.item_options=['examine','equip']
		self.options = ['%s' % self.to_str()]
		self.damage=1.0 * (25 * math.log(self.level + 1, 2) + 3) / 50.0
	def do_turn(self,option):
		self.options = ['%s' % self.to_str()]
		if option == self.options[0]:
			p = base.make_choice(['Shoot with %s' % self.to_str(), 'Fully draw the %s' % self.to_str(), 'Launch Volley'])
			if p == 0:
				target = self.owner.select_target()
				if target:
					self.shoot(target)
			elif p == 1:
				target = self.owner.select_target()
				if target:
					self.aim(target)
			elif p == 2:
				for a in self.owner.party.current_dungeon.active_room.things:
					if(isinstance(a,r.Monster) and a.revealed):
						self.volley(a)

	#an attempt to further increase the action points system. shoot would only cost 1 action point while aim would take 2
	def shoot(self,target):
		target.take_damage(self.owner,self.damage * self.owner.attributes['agility'] + self.owner.attributes['strength'] / 10.0 + base.D12.roll())
	def aim(self,target):
		target.take_damage(self.owner,self.damage * self.owner.attributes['agility'] * 1.9 + self.owner.attributes['strength']/4.0+base.D20.roll())
	def volley(self,target):
		target.take_damage(self.owner,self.damage*.1 + self.owner.attributes['agility']*.1+self.owner.attributes['strength']*.1+self.owner.attributes['intelligence']*.1+self.owner.attributes['luck']*.1)


class Rapier(Weapon):
	def __init__(self,level):
		super(Rapier,self).__init__()
		self.level=level
		self.name='rapier'
		self.info='one-handed'
		self.info2='weapon'
		self.item_options=['examine','equip']
		self.options = ['%s' % self.to_str()]
		self.damage = 2 * self.level

	def do_turn(self,option):
		self.options = ['%s' % self.to_str()]
		if option == self.options[0]:
			p = base.make_choice(['Slash with %s' % self.to_str(),'Pierce Armor with %s'%self.to_str()])
			if p == 0:
				target = self.owner.select_target()
				if target:
					self.slash(target)
			elif p==1:
				target = self.owner.select_target()
				if target:
					self.pierce(target)

	def slash(self,target):
		target.take_damage(self.owner,self.damage+self.owner.attributes['agility'])
	def pierce(self,target):
		hold=target.armor
		target.armor=0
		target.take_damage(self.owner,self.damage + self.owner.attributes['strength'] / 5.0 + self.owner.attributes['agility']/2.0 + self.owner.attributes['intelligence']/4.0 +hold+ base.D20.roll())
		target.armor=hold

class Flail(Weapon):
	def __init__(self,level):
		super(Flail,self).__init__()
		self.level = level

		self.name = 'flail'
		self.info='one-handed'
		self.info2='weapon'
		self.item_options=['examine','equip']
		self.options = ['%s' % self.to_str()]
		self.damage = 4.0 * self.level

	def do_turn(self,option):
		self.options = ['%s' % self.to_str()]
		if option == self.options[0]:
			p = base.make_choice(['attack with %s' % self.to_str()])
			if p == 0:
				target = self.owner.select_target()
				if target:
					self.swing(target)

	def swing(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['strength'] / 2.0 + self.owner.attributes['agility'] + self.owner.attributes['luck'] + base.D20.roll())

class Shield(Item):
	def __init__(self,level):
		super(Shield,self).__init__()
		self.name = 'shield'
		self.info='one-handed'
		self.info2='nope'
		self.level = level
		self.item_options=['examine','equip']
		self.options=['%s' % self.to_str()]
		self.armor=4*self.level
		self.defendin=False
		self.blockin=False

	#I am not sure how to do the do_turn method.
	def do_turn(self,option):
		self.options = ['%s' % self.to_str()]
		if self.defendin:
			for a in self.owner.party.inventory:
				a.armor-=(self.level*2)
			self.defendin=False
		if self.blockin:
			self.owner.armor-=(3*self.level)
			self.blockin=False
		if option == self.options[0]:
			p = base.make_choice(['Block with %s' % self.to_str(),'Defend Allies with %s' % self.to_str()])
			if p == 0:
				self.block()
			if p == 1:
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

	def get_cost(self):
		return self.cost * self.armor



class Breastplate(Item):
	def __init__(self,level):
		super(Breastplate,self).__init__()
		self.name = 'breastplate'
		self.info='chest'
		self.item_options=['examine','equip']
		self.level = level
		self.armor=20

	def apply(self):
		self.owner.armor += self.armor

	def exit(self):
		self.owner.armor -= self.armor

	def get_cost(self):
		return self.cost * self.armor


class Chainmail(Item):
	def __init__(self,level):
		super(Chainmail,self).__init__()
		self.name = 'chainmail'
		self.item_options=['examine','equip']
		self.info='chest'
		self.level = level
		self.armor=15
	def apply(self):
		self.owner.armor += self.armor

	def exit(self):
		self.owner.armor -= self.armor

	def get_cost(self):
		return self.cost * self.armor


class Platelegs(Item):
	def __init__(self,level):
		super(Platelegs,self).__init__()
		self.name = 'platelegs'
		self.item_options=['examine','equip']
		self.info='legs'
		self.level = level
		self.armor=12
	def apply(self):
		self.owner.armor += self.armor

	def exit(self):
		self.owner.armor -= self.armor

	def get_cost(self):
		return self.cost * self.armor


class Helmet(Item):
	def __init__(self,level):
		super(Helmet,self).__init__()
		self.name = 'helmet'
		self.info='helmet'
		self.item_options=['examine','equip']
		self.level = level
		self.armor=13
	def apply(self):
		self.owner.armor += self.armor

	def exit(self):
		self.owner.armor -= self.armor

	def get_cost(self):
		return self.cost * self.armor

class SpellBook(Item):
	def __init__(self,level):
		super(SpellBook,self).__init__()
		self.info = 'one-handed'
		self.info2='nope'
		self.cost = random.randint(0,10)
		# print type(level)

		self.level = level
		self.name = ''
		# hahahahahaha this is so fucking stupid
		for a in range(int(self.level)):
			self.name += "%s " % random.choice(arcane_words)
		self.options = ['%s' % self.name]
		self.stuntime = random.random() * (level * 4)
		self.poisontime = random.random() * (level * 4)
		self.damage = (random.random() * (20*level))
		self.poisondamage = (random.random() * (10*level)) - (5 * level)
		self.aoe = random.choice([True,False])
		self.on_cooldown = False
		self.cooldown_time = random.random() * (7 * level)
		self.item_options=['equip','examine']

	def do_turn(self,option):
		# effectiveness coefficient
		ec = self.owner.attributes['mana'] / 5
		if option == self.options[0]:
			p = base.make_choice(['cast %s' % self.name,'rename %s' % self.name,'examine %s' % self.name])
			if p == 1:
				name = raw_input('enter a new name for %s' % self.name)
				self.name = name
				self.options = ['%s' % self.name]

			if p == 2:
				print self.descr()

			if p == 0:
				if not self.on_cooldown:
					if not self.aoe:
						targets = [self.owner.select_target()]
					else:
						targets = self.owner.party.current_dungeon.active_room.things
					for target in targets:
						# we have to make sure that the targets are monsters, because otherwise we would hit chests and leaveoptions
						if target and isinstance(target,r.Monster):
							if self.damage:
								target.take_damage(self.owner,self.damage*ec)
							if self.stuntime:
								target.statuses.append(s.Stun(math.ceil(self.stuntime*ec)))
							if self.poisontime and self.poisondamage:
								target.statuses.append(s.Poison(math.ceil(self.poisontime*ec),self.poisondamage*ec))
					self.owner.statuses.append(s.Cooldown(self,self.cooldown_time))
				else:
					print '%s is on cooldown!' % self.name

	def to_str(self):
		return 'a spell by the name of %s' % self.name

	def descr(self):
		ret =  "%s does %.2f damage, stuns for %d turns and does %.2f of poison damage every turn for %d turns, with a cooldown of %d turns" % (self.name,self.damage,self.stuntime,self.poisondamage,self.poisontime,self.cooldown_time)
		if self.aoe:
			ret += 'in an area of effect.'
		else:
			ret += 'to a single target.'
		return ret

	def examine(self):
		return self.descr()

	def get_cost(self):
		return 20 * (10/self.cooldown_time)

# this extends item but overrides return_options to allow it to return an option
# if it isnt equipped
class Consumable(Item):
	def __init__(self):
		super(Consumable,self).__init__()

	def return_options(self):
		return self.options

class HealthPotion(Consumable):
	def __init__(self):
		super(HealthPotion,self).__init__()
		self.options = ['drink health potion']
		self.name = 'health potion'
		self.cost = 20
	def do_turn(self,option):
		# the player can only have one health potion active at a time
		if option == self.options[0] and not self.owner.statuses.contains_type(s.Healing):
			print "%s consumes a health potion!" % self.owner.name
			self.owner.statuses.append(s.Healing())
			self.owner.inventory.remove(self)

class Sack(Consumable):
	def __init__(self,contents):
		super(Sack,self).__init__()
		self.contents = contents
		self.options = ['open sack']
		self.name = 'a rugged sack'

	def do_turn(self,option):
		if option == 'open sack':
			de = ''
			for a in self.contents:
				self.owner.inventory.append(a)
				de += '%s, ' % a.name
			print 'you open the sack and find %s' % de[:-2]
			self.owner.inventory.remove(self)

class ItemController():
	def __init__(self,level):
		self.items = {
			'weapons':[Sword,Dagger,Bow,Flail,Rapier],
			'armor':[Shield,Breastplate,Chainmail,Platelegs,Helmet],
			'spells':[SpellBook],
			'health':[HealthPotion]
		}
		self.level = level
		self.applier = r.Apply()

	def generate(self,kind=None):
		if kind:
			if kind == 'weapons':
				return self.get_weapon()
			elif kind == 'armor':
				return self.get_armor()
			elif kind == 'spells':
				return self.get_spells()
		else:
			return random.choice([self.get_spells(),self.get_armor(),self.get_weapon(),self.get_health()])

	def get_weapon(self):
		weapon_instance = self.applier.modify_item(random.choice(self.items['weapons'])(self.level))
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
		armor_instance = self.applier.modify_item(random.choice(self.items['armor'])(self.level))
		return armor_instance

	def get_spells(self):
		spell_instance = SpellBook(self.level)
		return spell_instance

	def get_health(self):
		pot = Sack([HealthPotion(),HealthPotion(),HealthPotion()])
		return pot
