class Burrow(Entity):
	def __init__(self):
		super(Burrow,self).__init__()
		self.options = ['burrow','unburrow']

	def do_turn(self,options):
		if 'burrow' in options:
			if self.owner.statuses.contains(0)