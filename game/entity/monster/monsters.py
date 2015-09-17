import base


class Monster(base.Entity):
	def __init__(self):
		self.agro= None
		self.health = 100
		self.level=1
		self.power=self.level*10
		self.multiplier=1
		# base ap is what the ap should be restored to after a turn is complete
		self.base_ap = 3
		self.alive = True
		self.action_points = 3
		self.options = []
		self.inventory = Inventory(self)
		self.statuses = Inventory(self)
		self.owner = None

	def take_damage(self,val):
		pass
	def set_level(self,val):
		pass

class Skeleton(Monster):
	def __init__(self):
		self.health=50+self.level*20

class Goblin(Monster):
	def __init__(self):
		self.multiplier=.5
		self.power=self.level*4

class Spider(Monster):
	pass

class Assassin(Monster):
	def __init__(self):
		self.health=1
		self.multiplier=1.5
		self.power=20+self.level*25

class Hidden_Devourer(Monster):
	pass

class Goblin(Monster):
	pass

class Ogre(Monster)
	def __init__(self):
		self.health=200*self.level*40
		self.power=5+self.level*1;

class Hellhound(Monster):
	def __init__(self):
		self.health=100+self.level*25
		self.multiplier=1.1
		self.power=15+self.level*12

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