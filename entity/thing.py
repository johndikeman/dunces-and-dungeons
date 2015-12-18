import base


class InteractiveObject(base.Entity):
	def __init__(self):
		super(InteractiveObject,self).__init__()
		self.options = []

	def do_turn(self,option):
		pass

	def to_str(self):
		return 'some interactive object!'
