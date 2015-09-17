import base

class Monster(base.Entity):
	def __init__(self):
		self.agro= None
		self.health = 10

		# base ap is what the ap should be restored to after a turn is complete
		self.base_ap = 3
		self.alive = False
		self.action_points = 3
		self.options = []
		self.inventory = Inventory(self)
		self.statuses = Inventory(self)
		self.owner = None

class Skeleton(Monster):
	pass

class Spider(Monster):
	pass

class Assassin(Monster):
	pass

class Hidden_Devourer(Monster):
	pass

class Goblin(Monster):
	pass

class Ogre(Monster)
	pass

class Hellhound(Monster):
	pass

class Sorcerer(Monster):
	pass

class Elemental(Monster):
	pass

class Demigod(Monster):
	pass

class Overcharger(Monster):
	pass

class Cyclops(Monster):
	pass