import base
import entity.thing as t
import entity.item.items as items

class Chest(t.InteractiveObject):
	def __init__(self,level):
		super(Chest,self).__init__()
		self.level = level
		self.options = ['open chest']
		self.generator = items.ItemController(self.owner)
		self.items = [[]]

	def do_turn(self,option):
		if option == self.options[0]:
			inv = base.make_choice([i.to_str() for i in self.items])

	def to_str(self):
		return 'a chest!'

	def examine(self):
		return 'a chest'


def spawn(level):
	if base.D10.roll() <= 2:
		return Chest(level)
