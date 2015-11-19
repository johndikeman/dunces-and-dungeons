import base,math,random
import entity.status.player_statuses as s

# this is functionall the same thing as ItemUsedFromInventory except it doesnt inherit from item
# so it wont break InventoryHandler.
class Ability(base.Entity):
	def __init__(self):
		super(Ability,self).__init__()

	def return_options(self):
		return self.options

	def do_turn(self,option):
		if option is self.options[0]:
			self.main()

	def main(self):
		pass

	def to_str(self):
		return 'an ability'


# TANK
class BattleCry(Ability):
	def __init__(self):
		super(BattleCry,self).__init__()
		self.options = ['roar a primal roar']
		self.level = 1

	# roll a d10. if the roll is over 5, then you attract all the aggro of all the monsters
	def main(self):
		roll = base.D10.roll()
		if roll > 5:
			# if the roll is 10, you do damage to all monsters based on half your strength.
			if roll == 10:
				print 'primal roar critical success!'
				for a in self.owner.party.current_dungeon.active_room.things:
					a.aggro = self.owner
					a.take_damage(self.owner,self.owner.attributes['strength'] * .5)
			else:
				print 'primal roar successfully cast!'
				for a in self.owner.party.current_dungeon.active_room.things:
						a.aggro = self.owner
		# if the roll is one, you do the damage to all your party.
		elif roll == 1:
			print 'primal roar critical fail!'
			for party_member in self.owner.party.inventory:
				party_member.take_damage(self.owner,self.owner.attributes['strength'] * .5)
		else:
			print 'the primal roar was unsuccessful.'

# UNIMPLEMENTED
class ShieldBash(Ability):
	def __init__(self):
		super(ShieldBash,self).__init__()
		self.options = ['cast ShieldBash']
		self.level = 1

	def main(self):
		target = self.owner.select_target()
		if target:
			# TODO- implement stun
			target.statuses.append(s.Stun(2))

# TANK
class BerserkerVitality(Ability):
	def __init__(self):
		super(BerserkerVitality,self).__init__()
		self.options=[]
		self.level=1

	def do_turn(self,option):
		self.level = self.owner.level
		self.owner.health += self.level*.5
		print "%s's Berserker Vitality restores health!" % self.owner.name
		if self.owner.health > self.owner.max_health:
			self.owner.health = self.owner.max_health

# ROGUE
class Steal(Ability):
	def __init__(self):
		super(Steal,self).__init__()
		self.options=['pickpocket']
		self.level=1

	def do_turn(self,option):
		if option is self.options[0]:
			self.main()

	def main(self):
		target=self.owner.select_target()
		if target:
			amount=target.power/5
			roll=base.D20.roll()
			roll=roll+(self.owner.attributes['luck']/(100/self.owner.level))
			if roll>15:
				self.owner.gold = self.owner.gold + amount
				print 'successfully pickpocketed the %s for %d gold' % (target.name,amount)
			else:
				amo = (self.owner.max_health / 3 + target.power / 10)
				self.owner.health -= amo
				print 'critical failure pickpocketing! %s loses %d health!' % (self.owner.name,amo)

class Quickness(Ability):
	def __init__(self):
		super(Quickness,self).__init__()
		self.options = []

	def do_turn(self,option):
		if base.D10.roll() >= 9:
			self.main()

	def main(self):
		print '%s gets an extra action from their rogue quickness!' % self.owner.name
		self.owner.action_points += 1




# class ArcaneGenerator(base.Entity):
# 	def __init__(self):
# 		self.chromosomes = []
