class Player(Entity):
	def __init__(self,name):
		super(self,Player).__init__()
		self.inventory = {}
		self.name = name

	def return_options(self):
		li = []
		li += self.options
		for a in self.inventory.keys(): 
			li += self.inventory[a].return_options()
		return li

	def process_options(self,*args):
		for a in self.inventory.keys():
			self.inventory[a].process_options(args)




class Party(object):
	pass