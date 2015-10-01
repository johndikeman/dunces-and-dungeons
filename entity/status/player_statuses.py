import base

class Burrow(base.Entity):
	def __init__(self):
		super(BurrowStatus,self).__init__()

	def do_turn(self):
		pass


# TODO- implement Stun(turns_to_be_stunned)


class Stun(base.Entity):
	def __init__(self,turns):
		super(Stun,self).__init__()
		self.turns = turns

	def do_turn(self,options):
		print '%s is stunned, and cannot move!' % self.owner.to_str()
		if self.turns > 0:
			self.owner.action_points = 0
			self.turns -= 1
		else:
			self.owner.statuses.remove(self)


class Poison(base.Entity):
	def __init__(self,turns,damage):
		super(Poison,self).__init__()
		self.turns = turns
		self.damage = damage
		self.name = 'poison'

	def do_turn(self,option):
		if self.turns > 0:
			self.owner.health -= self.damage
			print '%s takes %f poison damage' % (self.owner.name,self.damage)
			self.turns -= 1
		else:
			self.owner.statuses.remove(self)

	def to_str(self):
		return self.name

class Cooldown(base.Entity):
	def __init__(self,spell,turns):
		super(Cooldown,self).__init__()
		self.spell = spell
		self.turns = turns
		self.spell.on_cooldown = True

	def do_turn(self,option):
		if self.turns > 0:
			self.turns -= 1
		else:
			self.spell.on_cooldown = False
			self.owner.statuses.remove(self)
