import base

class Item(base.Entity):
	def __init__(self):
		super(Item,self).__init__()
		self.consumes_inventory_space = True

	def to_str(self):
		return "this is the item superclass. if you're reading this you really shouldn't be"

	def do_turn(self,options):
		pass

class Sword(Item):
	def __init__(self):
		super(Sword,self).__init__()
		self.options = ['swing %s' % self]

	def do_turn(self,options):
		if self.options[0] in options:
			target_ind = base.make_choice(self.owner.party.dungeon.current_room.contents,'target')
			self.swing(self.owner.party.dungeon.current_room.contents[target_ind])

	def swing(self,target):




	def to_str(self):
		return 'sword'
