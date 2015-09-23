import base
# warrior
# level one abilities

class BattleCry(base.Entity):
	def __init__(self):
		super(BattleCry,self).__init__()
		self.options = ['cast BattleCry']
		self.level = 1

	# roll a d10. if the roll is over 5, then you attract all the aggro of all the monsters
	def do_turn(self,option):
		if option == self.options[0]:
			roll = base.D10.roll()
			if roll > 5:
				# if the roll is 10, you do damage to all monsters based on half your strength.
				if roll == 10:
					print 'BattleCry critical success!'
					for a in self.owner.current_dungeon.current_room.things:
						a.aggro = self.owner
						a.take_damage(self.owner,self.owner.attributes['strength'] * .5)
				else:	
					print 'BattleCry successfully cast!'
					for a in self.owner.current_dungeon.current_room.things:
							a.aggro = self.owner
			# if the roll is one, you do the damage to all your party.
			elif roll == 1:
				print 'BattleCry critical fail!'
				for party_member in self.owner.party.inventory:
					party_member.take_damage(self.owner,self.owner.attributes['strength'] * .5)


class ShieldBash(base.Entity):
	def __init__(self):
		super(BattleCry,self).__init__()
			self.options = ['cast ShieldBash']
			self.level = 1

	def do_turn(self,option):
		pass


