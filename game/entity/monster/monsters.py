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
		self.power=10+self.level*10

class Goblin(Monster):
	def __init__(self):
		self.health=20+self.level*4
		self.multiplier=.5
		self.power=self.level*4

class Spider(Monster):
	def __init__(self):
		self.multiplier=.4
		self.power=2+self.level*1

class Assassin(Monster):
	def __init__(self):
		self.health=1+self.level*5
		self.multiplier=1.5
		self.power=20+self.level*25

class Hidden_Devourer(Monster):
	def __init__(self):
		self.health=5+self.level*3
		self.multiplier=.6
		self.power=20+self.level*30
		self.ap=1
		self.action_points=1


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
	def __init__(self):
		self.health=75+self.level*10
		self.multiplier = .9
		self.power=25+self.level*10

class Elemental(Monster):
	def __init__(self):
		self.health=60+self.level*20
		self.power=20+self.level*7

class WindElemental(Elemental):
	def __init__(self):
		self.health=40+self.level*10
		self.power=10+self.level*9

class WaterElemental(Elemental):
	def __init__(self):
		self.power=15+self.level*10

class FireElemental(Elemental):
	def __init__(self):
		self.health=30+self.level*12
		self.power=30+self.level*12

class EarthElemental(Elemental):
	def __init__(self):
		self.health=100+self.level*20
		self.power=15+self.level*8

class Demigod(Monster):
	def __init__(self):
		self.multiplier=1.6
		self.health=200+self.level*18
		self.power=25+self.level*14
		self.action_points=2

class Overcharger(Monster):
	def __init__(self):
		self.multiplier=1.05
		self.health=80+self.level*10
		self.power=50+self.level*30
		self.ap=1
		self.action_points=1

class Cyclops(Monster):
	def __init__(self):
		self.health=80+self.level*20
		self.power=20+self.level*10