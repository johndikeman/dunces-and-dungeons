import base





class Monster(base.Entity):
	def __init__(self,level):
		self.aggro = None
		self.aggroed = False
		self.probablity = 0.0

		# this is the potential size of the group
		self.groupsize = range(2)


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

	def take_damage(self,attacker,val):
		print '(%s) takes (%d) damage from (%s)' % (self.to_str(),damage,attacker.to_str())

		self.health -= val
		if self.hp <= 0:
			self.alive = False
			print "(%s) has died by the hand of (%s)" % (self.to_str(),attacker.to_str())

	def set_level(self,val):
		pass

	def do_turn(self):
		for a in self.owner.party:
			if not self.aggroed:
				self.aggro = a
			else:
				attack(self.aggro)

	def attack(self,target):
		target.take_damage(0)

	def to_str(self):
		return 'hmMm looks like SOMEONE didn\'t implement this method in the monster they designed!'


class Skeleton(Monster):
	def __init__(self,level):
		super(Skeleton,self).__init__(level)
		self.health=50+self.level*20
		self.power=10+self.level*10
		self.probablity = 1.0

class Goblin(Monster):
	def __init__(self,level):
		super(Goblin,self).__init__(level)
		self.health=20+self.level*4
		self.multiplier=.5
		self.power=self.level*4

class Spider(Monster):
	def __init__(self,level):
		super(Spider,self).__init__(level)
		self.multiplier=.4
		self.power=2+self.level*1

class Assassin(Monster):
	def __init__(self,level):
		super(Assassin,self).__init__(level)
		self.health=1+self.level*5
		self.multiplier=1.5
		self.power=20+self.level*25

class Hidden_Devourer(Monster):
	def __init__(self,level):
		super(Hidden_Devourer,self).__init__(level)
		self.health=5+self.level*3
		self.multiplier=.6
		self.power=20+self.level*30
		self.ap=1
		self.action_points=1


class Ogre(Monster)
	def __init__(self,level):
		super(Ogre,self).__init__(level)
		self.health=200*self.level*40
		self.power=5+self.level*1;

class Hellhound(Monster):
	def __init__(self,level):
		super(Hellhound,self).__init__(level)
		self.health=100+self.level*25
		self.multiplier=1.1
		self.power=15+self.level*12

class Sorcerer(Monster):
	def __init__(self,level):
		super(Sorcerer,self).__init__(level)
		self.health=75+self.level*10
		self.multiplier = .9
		self.power=25+self.level*10

class Elemental(Monster):
	def __init__(self,level):
		super(Elemental,self).__init__(level)
		self.health=60+self.level*20
		self.power=20+self.level*7

class WindElemental(Elemental):
	def __init__(self,level):
		super(WindElemental,self).__init__(level)
		self.health=40+self.level*10
		self.power=10+self.level*9

class WaterElemental(Elemental):
	def __init__(self,level):
		super(WaterElemental,self).__init__(level)
		self.power=15+self.level*10

class FireElemental(Elemental):
	def __init__(self,level):
		super(FireElemental,self).__init__(level)
		self.health=30+self.level*12
		self.power=30+self.level*12

class EarthElemental(Elemental):
	def __init__(self,level):
		super(EarthElemental,self).__init__(level)
		self.health=100+self.level*20
		self.power=15+self.level*8

class Demigod(Monster):
	def __init__(self,level):
		super(Demigod,self).__init__(level)
		self.multiplier=1.6
		self.health=200+self.level*18
		self.power=25+self.level*14
		self.action_points=2

class Overcharger(Monster):
	def __init__(self,level):
		super(Overcharger,self).__init__(level)
		self.multiplier=1.05
		self.health=80+self.level*10
		self.power=50+self.level*30
		self.ap=1
		self.action_points=1

class Cyclops(Monster):
	def __init__(self,level):
		super(Cyclops,self).__init__(level)
		self.health=80+self.level*20
		self.power=20+self.level*10


MONSTERLIST = {
	Skeleton:{
		"probablity":100.0,
		'groupsize':3
	},
}

def spawn():
	for key, val in MONSTERLIST.iteritems():
		pass
