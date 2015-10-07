import base

class Chest(base.Entity):
	def __init__(self,level):
		super(Chest,self).__init__()
		self.level = level

	def do_turn(self):
		pass