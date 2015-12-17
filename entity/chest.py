import base
import entity.thing as t
import entity.item.controller as control
import random
import math


class Chest(t.InteractiveObject):
	def __init__(self,level):
		super(Chest,self).__init__()
		self.level = level
		self.options = ['open chest']
		self.generator = control.ItemController(self.level)
		self.items = []
								# this got out of hand fast
		for a in range((int(math.ceil(5)))):
			self.items.append(self.generator.generate())


	def do_turn(self,option):
		if option == self.options[0]:
			inv = base.make_choice([i.to_str() for i in self.items])
			if inv is not None:
				self.owner.containing_dungeon.party.get_active_player().add_to_inventory(self.items[inv])
				self.items = self.items[:inv] + self.items[inv+1:]

	def to_str(self):
		return 'a chest!'

	def examine(self,examiner):
		return 'a chest'


def spawn(level):
	if base.D10.roll() <= 2:
		return Chest(level)
