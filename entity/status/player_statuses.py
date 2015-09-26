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

