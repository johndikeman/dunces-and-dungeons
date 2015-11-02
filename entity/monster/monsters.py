import base, random, time
import entity.modifier as mo
import entity.monster.monster_modification as mod
class Monster(base.Entity):
	def __init__(self,level):
		super(Monster,self).__init__()
		self.name="Monster"
		self.aggro = None
		self.aggroed = False
		self.probablity = 0.0

		self.health = 100
		self.level=1
		self.power=self.level*10.0
		self.multiplier=1
		# base ap is what the ap should be restored to after a turn is complete
		self.base_ap = 1
		self.alive = True
		self.action_points = 1
		self.options = []
		self.inventory = base.Inventory(self)
		self.statuses = base.Inventory(self)
		self.owner = None
		self.revealed = False
		self.xp_reward = self.level * 10


	def set_level(self,val):
		pass

	def select_aggro(self):
		self.aggro = random.choice(self.owner.party.inventory)
		self.aggroed = True

	def check_if_alive(self):
		if self.health <= 0:
			self.kill()

	def do_turn(self):
		for a in self.statuses:
			a.do_turn([])
		self.check_if_alive()

		if self.action_points > 0:
			if not self.aggroed:
				self.select_aggro()

			if self.aggro.alive:
				self.attack(self.aggro)
				for a in self.modifiers:
					a.do_turn(self.aggro)
			self.action_points -= 1

	def attack(self,target):
		self.reveal()
		target.take_damage(self,self.power)
		self.take_damage(target,target.retaliate())

	def to_str(self):
		return self.name

	def examine(self,examiner):
		self.reveal()
		return self.to_str()

	def reveal(self):
		if not self.revealed:
			self.revealed = True

	def dev_examine(self):
		print 'name: %s health: %d, attributes: %s, power: %s, level: %d' % (self.name, self.health,str(self.attributes),self.power,self.level)

	def kill(self,killa=None):
		self.alive = False
		if killa:
			killa.update_xp(self.xp_reward)
		self.owner.things.remove(self)

def compute(comp,val):
	fin = 1.0
	for a in comp:
		fin *= a
	return (fin * (val / 100.0))

def spawn(level):
	ind = 0
	app=mo.Apply()
	ret = []
	compound = []
	while ind < len(MONSTERLIST.keys()):
		key = random.choice(MONSTERLIST.keys())
		val = MONSTERLIST[key]
		if random.random() * 100 < compute(compound,val['probability'])*100.0:
			compound.append(val['probability'] / 100.0)
			for x in range(random.choice(range(val['groupsize']))+1):
				ret.append(app.modify_monster(key(level)))
		ind += 1
	return ret

class Skeleton(Monster):
	def __init__(self,level):
		super(Skeleton,self).__init__(level)
		self.health=10+self.level*8
		self.power=4+(self.level-1)*4
		self.name="Skeleton"

	def to_str(self):
		return self.name

class Goblin(Monster):
	def __init__(self,level):
		super(Goblin,self).__init__(level)
		self.health=8+self.level*6
		self.multiplier=.5
		self.power=3+(self.level-1)*4
		self.name="Goblin"

## Hmmmmm..... My spiders health change has disappearrf
class Spider(Monster):
	def __init__(self,level):
		super(Spider,self).__init__(level)
		self.health=10+self.level*3
		self.multiplier=.4
		self.power=2+(self.level-1)*.5
		self.name="Spider"

class Assassin(Monster):
	def __init__(self,level):
		super(Assassin,self).__init__(level)
		self.health=1+self.level*3
		self.multiplier=1.5
		self.power=10+(self.level-1)*15
		self.name="Assassin"

class Hidden_Devourer(Monster):
	def __init__(self,level):
		super(Hidden_Devourer,self).__init__(level)
		self.health=5+self.level*3
		self.multiplier=.6
		self.power=8+(self.level-1)*12
		self.ap=1
		self.action_points=1
		self.name="Hidden Devourer"


class Ogre(Monster):
	def __init__(self,level):
		super(Ogre,self).__init__(level)
		self.health=50+self.level*25
		self.power=1+(self.level-1)*2;
		self.name="Ogre"

class Hellhound(Monster):
	def __init__(self,level):
		super(Hellhound,self).__init__(level)
		self.health=40+self.level*15
		self.multiplier=1.1
		self.power=12+(self.level-1)*10
		self.name="Hellhound"

class Sorcerer(Monster):
	def __init__(self,level):
		super(Sorcerer,self).__init__(level)
		self.health=12+self.level*8
		self.multiplier = .9
		self.power=15+(self.level-1)*10
		self.name="Sorcerer"

class Elemental(Monster):
	def __init__(self,level):
		super(Elemental,self).__init__(level)
		self.health=20+self.level*15
		self.power=15+(self.level-1)*7
		self.name="Elemental"
class Meme(Monster):
	def __init__(self,level):
		super(Meme,self).__init__(level)
		self.health=420+self.level*9.11
		self.power=69+(self.level-1)*42
		self.name ="Meme"
class WindElemental(Elemental):
	def __init__(self,level):
		super(WindElemental,self).__init__(level)
		self.health=5+self.level*10
		self.power=11+(self.level-1)*9
		self.name="Wind Elemental"

class WaterElemental(Elemental):
	def __init__(self,level):
		super(WaterElemental,self).__init__(level)
		self.power=4+(self.level-1)*13
		self.name="Water Elemental"

class FireElemental(Elemental):
	def __init__(self,level):
		super(FireElemental,self).__init__(level)
		self.modif=[mod.Scorched, mod.Dank]
		self.health=10+self.level*12
		self.power=18+(self.level-1)*12
		self.name="Fire Elemental"

# here down are not added to the spawn list

class EarthElemental(Elemental):
	def __init__(self,level):
		super(EarthElemental,self).__init__(level)
		self.modif=[mod.Acidic, mod.Caustic, mod.Decaying, mod.Destructive, mod.Dieing, mod.Flowery, mod.Forgotten, mod.Foul, mod.Musky, mod.Nasty, mod.Normal, mod.Rancid, mod.Scorched]
		self.health=100+self.level*20
		self.power=4+(self.level-1)*8
		self.name="Earth Elemental"

class Demigod(Monster):
	def __init__(self,level):
		super(Demigod,self).__init__(level)
		self.modif=[mod.Camphoric, mod.Dank, mod.Destructive, mod.Forgotten, mod.Funky, mod.Lightning, mod.Nasty]
		self.multiplier=1.6
		self.health=100+self.level*18
		self.power=20+(self.level-1)*14
		self.action_points=2
		self.name="Demigod"

class Overcharger(Monster):
	def __init__(self,level):
		super(Overcharger,self).__init__(level)
		self.modif=[mod.Dank, mod.Destructive, mod.Forgotten, mod.Funky, mod.Lightning, mod.Nasty]
		self.multiplier=1.05
		self.health=5+self.level*5
		self.power=30+(self.level-1)*40
		self.ap=1
		self.action_points=1
		self.name="Overcharger"

class Cyclops(Monster):
	def __init__(self,level):
		super(Cyclops,self).__init__(level)
		self.modif=[mod.Tiny, mod.Camphoric, mod.Caustic, mod.Dank, mod.Destructive, mod.Dieing, mod.Forgotten, mod.Lowly, mod.Musky, mod.Nasty, mod.Normal, mod.Weak]
		self.health=60+self.level*15
		self.power=6+(self.level-1)*10
		self.name="Cyclops"


MONSTERLIST = {
	Skeleton:{
		'probability':40.0,
		'groupsize':3
	},
	Goblin:{
		'probability':30.0,
		'groupsize':6
	},
	Spider:{
		'probability':25.0,
		'groupsize':12
	},
	Assassin:{
		'probability':4.0,
		'groupsize':1
	},
	Hidden_Devourer:{
		'probability':6.0,
		'groupsize':1
	},
	Ogre:{
		'probability':20.0,
		'groupsize':2
	},
	Hellhound:{
		'probability':5.0,
		'groupsize':2
	},
	Sorcerer:{
		'probability':8.0,
		'groupsize':1
	},
	Meme:{
		'probability':.001,
		'groupsize':3
	},
	WindElemental:{
		'probability':15.0,
		'groupsize':4
	},
	WaterElemental:{
		'probability':12.0,
		'groupsize':3
	},
	FireElemental:{
		'probability':10.0,
		'groupsize':3
	},
	EarthElemental:{
		'probability':12.0,
		'groupsize':2
	},
	Demigod:{
		'probability':.5,
		'groupsize':1
	},
	Overcharger:{
		'probability':5.0,
		'groupsize':2
	},
	Cyclops:{
		'probability':8.0,
		'groupsize':3
	}
}
