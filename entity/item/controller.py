import random
import entity.item.weapon as weapon
import entity.item.consumable as consumable
import entity.item.armor as armor
import entity.item.items as item
import entity.monster.monsters as r
import entity.modifier as m
import entity.item.utils as utils



class ItemController():
	def __init__(self,level):
		self.items = {
			'weapons':[weapon.Sword,weapon.Dagger,weapon.Bow,weapon.Flail,weapon.Rapier],
			'armor':[armor.Shield,armor.Breastplate,armor.Chainmail,armor.Platelegs,armor.Helmet],
			'spells':[item.SpellBook],
			'health':[consumable.HealthPotion]
		}
		self.level = level
		self.applier = m.Apply()

	def generate(self,kind=None):
		if kind:
			if kind == 'weapons':
				return self.get_weapon()
			elif kind == 'armor':
				return self.get_armor()
			elif kind == 'spells':
				return self.get_spells()
			elif kind == 'utility':
				return self.get_utils()
		else:
			return random.choice([self.get_spells(),self.get_armor(),self.get_weapon(),self.get_health()])

	def get_utils(self):
		return random.choice([utils.Map(),utils.CompletedMap()])

	def get_weapon(self):
		weapon_instance = self.applier.modify_weapon(random.choice(self.items['weapons'])(self.level))
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
		armor_instance = self.applier.modify_armor(random.choice(self.items['armor'])(self.level))
		return armor_instance

	def get_spells(self):
		spell_instance = item.SpellBook(self.level)
		return spell_instance

	def get_health(self):
		pot = consumable.Sack([consumable.HealthPotion(),consumable.HealthPotion(),consumable.HealthPotion()])
		return pot
