import base,random,math
from misc.words import arcane_words, weapon_words
import entity.status.player_statuses as s
import entity.monster.monsters as r
import entity.item.weapon as weapon
import entity.item.consumable as consumable
import entity.item.armor as armor


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

class ItemController():
	def __init__(self,level):
		self.items = {
			'weapons':[weapon.Sword,weapon.Dagger,weapon.Bow,weapon.Flail,weapon.Rapier],
			'armor':[armor.Shield,armor.Breastplate,armor.Chainmail,armor.Platelegs,armor.Helmet],
			'spells':[SpellBook],
			'health':[consumable.HealthPotion]
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
		pot = Sack([entity.item.consumable.HealthPotion(),entity.item.consumable.HealthPotion(),entity.item.consumable.HealthPotion()])
		return pot
