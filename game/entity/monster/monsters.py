import base, random

SMELL = ('acidic acrid aromatic camphoric fetid flowery foul fragrant fresh funky heady musky musty nasty noxious perfumed piney pungent rancid savory sharp smelly stinky stuffy sweet'.split(' '))
Mod={"acidic":{"health":"*.5"},
	 "acrid":{},
	 "aromatic":{},
	 "camphoric":{},
	 "fetid":{},
	 "flowery":{},
	 "foul":{},
	 "fragrant":{},
	 "fresh":{},
	 "funky":{},
	 "heady":{},
	 "musky":{},
	 "musty":{},
	 "nasty":{},
	 "noxious":{},
	 "perfumed":{},
	 "piney":{},
	 "pungent":{},
	 "rancid":{},
	 "savory":{},
	 "sharp":{},
	 "smelly":{},
	 "stinky":{},
	 "stuffy":{},
	 "sweet":{}}
class Apply(object):
	def modify_monster(Monster):
		namer=random.choice(SMELL)
		run=Mod[namer]
		for a in run:
			if(a=="health"):
				if(run[a][0]=="+"):
					Monster.health=Monster.health+float(run[a][0:len(run[a])])
				elif(run[a][0]=="*"):
					Monster.health=Monster.health*float(run[a][0:len(run[a])])
			elif(a=="power"):
				if(run[a][0]=="+"):
					Monster.power=Monster.power+float(run[a][0:len(run[a])])
				elif(run[a][0]=="*"):
					Monster.power=Monster.power*float(run[a][0:len(run[a])])
			elif(a=="level"):
				if(run[a][0]=="+"):
					Monster.level=Monster.level+float(run[a][0:len(run[a])])
				elif(run[a][0]=="*"):
					Monster.level=Monster.level*float(run[a][0:len(run[a])])
			elif(a=="ap"):
				if(run[a][0]=="+"):
					Monster.action_points=Monster.action_points+float(run[a][0:len(run[a])])
				elif(run[a][0]=="*"):
					Monster.health=Monster.health*float(run[a][0:len(run[a])])
			elif(a=="baseap"):
				if(run[a][0]=="+"):
					Monster.health=Monster.health+float(run[a][0:len(run[a])])
				elif(run[a][0]=="*"):
					Monster.health=Monster.health*float(run[a][0:len(run[a])])



class Monster(base.Entity):
	def __init__(self,level):
		self.aggro = None
		self.aggroed = False
		self.probablity = 0.0

		self.health = 100
		self.level=1
		self.power=self.level*10
		self.multiplier=1
		# base ap is what the ap should be restored to after a turn is complete
		self.base_ap = 3
		self.alive = True
		self.action_points = 3
		self.options = []
		self.inventory = base.Inventory(self)
		self.statuses = base.Inventory(self)
		self.owner = None

	def take_damage(self,attacker,val):
		print '(%s) takes (%d) damage from (%s)' % (self.to_str(),val,attacker.to_str())
		self.health -= val
		if self.health <= 0:
			self.alive = False
			print "(%s) has died by the hand of (%s)" % (self.to_str(),attacker.to_str())

	def set_level(self,val):
		pass

	def do_turn(self):
		if not self.aggroed:
			self.aggro = random.choice(self.owner.party.inventory)
		self.aggroed = True
				
		self.attack(self.aggro)

	def attack(self,target):
		target.take_damage(self,0)

	def to_str(self):
		return 'hmMm looks like SOMEONE didn\'t implement this method in the monster they designed!'
def spawn(level):
	ret = []
	for key, val in MONSTERLIST.iteritems():
		if random.random() * 100 < val['probablity']:
			for x in range(random.choice(range(val['groupsize']))+1):
				ret.append(key(level))
	return ret

class Skeleton(Monster):
	def __init__(self,level):
		super(Skeleton,self).__init__(level)
		self.health=50+self.level*20
		self.power=10+self.level*10

	def to_str(self):
		return 'skeleton'

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


class Ogre(Monster):
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
		'probablity':100.0,
		'groupsize':3
	},
}

