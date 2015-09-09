import base
class Player(base.Entity):
	def __init__(self,name):
		super(Player,self).__init__()
		self.name = name
		
	def process_options(self,*args):
		for a in self.inventory.keys():
			self.inventory[a].process_options(args)




class Party(object):
	pass