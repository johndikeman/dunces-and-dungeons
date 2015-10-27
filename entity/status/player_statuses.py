import base

class Burrow(base.Entity):
	def __init__(self):
		super(BurrowStatus,self).__init__()

	def do_turn(self):
		pass


# TODO- implement Stun(turns_to_be_stunned)

class Healing(base.Entity):
	def __init__(self):
		super(Healing,self).__init__()
		self.turns = 5

	def do_turn(self,options):
		if self.turns > 0:
			hp_restored = self.owner.max_health * .10
			self.owner.health += hp_restored
			if self.owner.health > self.owner.max_health:
				self.owner.health = self.owner.max_health
			print "healed %s for %d" % (self.owner.name, hp_restored)
			self.turns -= 1
		else:
			self.owner.statuses.remove(self)



class Stun(base.Entity):
	def __init__(self,turns):
		super(Stun,self).__init__()
		self.turns = turns

	def do_turn(self,options):
		print '%s is stunned, and cannot move for another %d turns' % (self.owner.to_str(),self.turns)
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

class Burn(base.Entity):
	def __init__(self,turns,damage):
		super(Burn,self).__init__()
		self.turns = turns
		self.damage = damage
		self.name = 'burn'

	def do_turn(self,option):
		if self.turns > 0:
			self.owner.health -= self.damage
			print '%s takes %f burn damage' % (self.owner.name,self.damage)
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
