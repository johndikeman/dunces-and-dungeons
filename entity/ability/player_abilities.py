import base,math,random
import entity.status.player_statuses as s

# this is functionall the same thing as ItemUsedFromInventory except it doesnt inherit from item
# so it wont break InventoryHandler.
class Ability(base.Entity):
	def __init__(self):
		super(Ability,self).__init__()

	def return_options(self):
		return self.options


class BattleCry(Ability):
	def __init__(self):
		super(BattleCry,self).__init__()
		self.options = ['roar a primal roar']
		self.level = 1

	# roll a d10. if the roll is over 5, then you attract all the aggro of all the monsters
	def do_turn(self,option):
		if option == self.options[0]:
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


class ShieldBash(Ability):
	def __init__(self):
		super(BattleCry,self).__init__()
		self.options = ['cast ShieldBash']
		self.level = 1

	def do_turn(self,option):
		target = self.owner.select_target()
		if target:
			# TODO- implement stun
			target.statuses.append(s.Stun(2))



# class ArcaneGenerator(base.Entity):
# 	def __init__(self):
# 		self.chromosomes = []
