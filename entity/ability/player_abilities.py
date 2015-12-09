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
				self.owner.do_aoe_monster(self.action_damage)
			else:
				print 'primal roar successfully cast!'
				self.owner.do_aoe_monster(self.action)
		# if the roll is one, you do the damage to all your party.
		elif roll == 1:
			print 'primal roar critical fail!'
			for party_member in self.owner.party.inventory:
				party_member.take_damage(self.owner,self.owner.attributes['strength'] * .5)
		else:
			print 'the primal roar was unsuccessful.'

	def action(self,monster):
		monster.aggro = self.owner

	def action_damage(self,monster):
		monster.aggro = self.owner
		monster.take_damage(self.owner,self.owner.attributes['strength'] * .5)

#Ranger
class Perseverance(Ability):
	def __init__(self):
		super(Perseverance,self).__init__()
		self.level=1
		self.count=0

	def do_turn(self,option):
		self.level=self.owner.level/10.0
		self.main()

	def main(self):
		self.count+=1
		if self.count == 10:
			self.owner.armor+=self.level
			self.count=0

class Swap(Ability):
	def __init__(self):
		super(Swap,self).__init__()
		self.level=1
		self.options = ['cast Swap']

	def do_turn(self,option):
		if option is self.options[0]:
			self.main()

	def main(self):
		target=self.owner.select_target()
		roll=base.D20.roll()
		if roll<11:
			stat=[]
			for a in self.owner.statuses:
				a.owner=target
				stat.append(a)
			self.owner.statuses=[]
			stat1=[]
			for a in target.statuses:
				a.owner=self.owner
				stat1.append[a]
			target.statuses=[]
			self.owner.statuses=stat1
			target.statuses=stat
			#target.statuses, self.owner.statuses = self.owner.statuses, target.statuses
			print 'You successfully swap your statuses with the Enemies!'
		else:
			times=len(self.owner.statuses)
			print 'Woops! You doubled your own statuses!'
			for a in range(times):
				self.owner.statuses.append(self.owner.statuses[a])



# Wizard
class Dementia(Ability):
	def __init__(self):
		super(Dementia,self).__init__()
		self.options = ['cast Dementia']
		self.level=1

	def do_turn(self,option):
		if option is self.options[0]:
			self.main()

	def main(self):
		self.level=self.owner.level
		self.owner.do_aoe_monster(self.action)

	def action(self,mon):
		if self.level/2 > mon.level:
			mon.aggroed=False
			mon.aggro=None
		roll=base.D100.roll()
		roll2=base.D20.roll()
		if roll2>10 and self.level>roll:
			mon.aggroed=False
			mon.aggro=None

class Forget(Ability):
	def __init__(self):
		super(Forget,self).__init__()
		self.level=1

	def do_turn(self,option):
		self.main()
	def main(self):
		roll=base.D20.roll()
		if roll < 4:
			print"You forget what you were planning on doing!"
			self.owner.action_points=0

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
