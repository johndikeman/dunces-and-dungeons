import base, random, time
import entity.modifier as mo
import entity.monster.monster_modification as mod
import math

class Monster(base.Entity):
	def __init__(self,level):
		super(Monster,self).__init__()
		self.name="Monster"
		self.aggro = None
		self.aggroed = False
		self.probablity = 0.0
		self.room=None
		self.health = 100
		self.level = level
		self.power = self.level * 10.0
		self.multiplier = 1
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

		# this will be used in especially strong modifiers to make the rewards higher.
		self.generic_reward_multiplier = 1.0

	# for computing rewards after the specific monster and modifier applications.
	def compute_rewards(self):
		self.xp_reward = math.pow(abs(self.level * 10 * (self.power / 3) * self.generic_reward_multiplier),.8)

	def set_level(self,val):
		pass

	def select_aggro(self):
		self.aggro = random.choice(self.owner.party.inventory)
		self.aggroed = True

	def check_if_alive(self):
		if self.health <= 0:
			self.kill()
			return True

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
		self.take_damage(target,target.retaliate(self))

	def conceal(self):
		self.revealed=False
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
		#self.owner.things.remove(self)

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

# this is a special monster that spider queen spawns. dont add it to room spawnlists.
class Spiderling(Monster):
	def __init__(self,level):
		super(Spiderling,self).__init__(level)
		self.max_health=self.level*10
		self.health = self.level * 10
		self.power = self.level * 10
		self.name = "Spiderling"

	def do_turn(self):
		super(Spiderling,self).do_turn()
		if base.D6.roll() == 1:
			print 'a spiderling has reproduced!'
			child = Spiderling(self.level)
			child.action_points = 0
			self.owner.things.append(child)

class Skeleton(Monster):
	def __init__(self,level):
		super(Skeleton,self).__init__(level)
		self.modif=[mod.Acidic,mod.Caustic,mod.Dieing,mod.Dusty,mod.Fetid,mod.Foul,mod.Lowly,mod.Normal, mod.Putrid,mod.Tiny, mod.Weak,mod.Rancid,mod.Dieing]
		self.max_health=10+self.level*12
		self.health=10+self.level*12
		self.power=4+(self.level-1)*7
		self.name="Skeleton"
		# self.compute_rewards()

	def to_str(self):
		return self.name

class Goblin(Monster):
	def __init__(self,level):
		super(Goblin,self).__init__(level)
		self.modif=[mod.Acidic,mod.Caustic,mod.Dieing,mod.Dusty,mod.Fetid,mod.Foul,mod.Lowly,mod.Normal, mod.Putrid,mod.Tiny, mod.Weak]
		self.max_health=8+self.level*9
		self.health=8+self.level*9
		self.multiplier=.5
		self.power=3+(self.level-1)*7
		self.name="Goblin"
		# self.compute_rewards()

## Hmmmmm..... My spiders health change has disappearrf
class Spider(Monster):
	def __init__(self,level):
		super(Spider,self).__init__(level)
		self.modif=[mod.Acidic,mod.Caustic,mod.Dieing,mod.Dusty,mod.Fetid,mod.Foul,mod.Lowly,mod.Normal, mod.Putrid,mod.Tiny, mod.Weak]
		self.max_health=10+self.level*6
		self.health=10+self.level*6
		self.multiplier=.4
		self.power=2+(self.level-1)
		self.name="Spider"
		# self.compute_rewards()

class Assassin(Monster):
	def __init__(self,level):
		super(Assassin,self).__init__(level)
		self.modif=[mod.Dank,mod.Destructive,mod.Funky,mod.Lightning,mod.Musky,mod.Nasty,mod.Camphoric]
		self.max_health=1+self.level*9
		self.health=1+self.level*9
		self.multiplier=1.5
		self.power=10+(self.level-1)*22
		self.name="Assassin"
		# self.compute_rewards()

class Hidden_Devourer(Monster):
	def __init__(self,level):
		super(Hidden_Devourer,self).__init__(level)
		self.modif=[mod.Dank,mod.Lowly, mod.Destructive,mod.Musky,mod.Nasty,mod.Lightning,mod.Forgotten]
		self.max_health=5+self.level*8
		self.health=5+self.level*8
		self.multiplier=.6
		self.power=8+(self.level-1)*19
		self.ap=1
		self.action_points=1
		self.name="Hidden Devourer"
		# self.compute_rewards()


class Ogre(Monster):
	def __init__(self,level):
		super(Ogre,self).__init__(level)
		self.modif=[mod.Forgotten,mod.Musky, mod.Normal, mod.Tiny, mod.Camphoric]
		self.max_health=50+self.level*35
		self.health=50+self.level*35
		self.power=1+(self.level-1)*3;
		self.name="Ogre"
		# self.compute_rewards()

class Hellhound(Monster):
	def __init__(self,level):
		super(Hellhound,self).__init__(level)
		self.modif=[mod.Destructive,mod.Lightning,mod.Dank,mod.Scorched,mod.Musky,mod.Nasty]
		self.max_health=40+self.level*25
		self.health=40+self.level*25
		self.multiplier=1.1
		self.power=12+(self.level-1)*18
		self.name="Hellhound"
		# self.compute_rewards()

class Sorcerer(Monster):
	def __init__(self,level):
		super(Sorcerer,self).__init__(level)
		self.modif=[mod.Caustic, mod.Dank, mod.Destructive, mod.Forgotten, mod.Funky, mod.Lowly, mod.Nasty]
		self.max_health=12+self.level*12
		self.health=12+self.level*12
		self.multiplier = .9
		self.power=15+(self.level-1)*15
		self.name="Sorcerer"
		# self.compute_rewards()

class Elemental(Monster):
	def __init__(self,level):
		super(Elemental,self).__init__(level)
		self.max_health=20+self.level*22
		self.health=20+self.level*22
		self.power=15+(self.level-1)*10
		self.name="Elemental"
		# self.compute_rewards()
class Meme(Monster):
	def __init__(self,level):
		super(Meme,self).__init__(level)
		self.modif=[mod.Dank, mod.Forgotten]
		self.max_health=420+self.level*9.11
		self.health=420+self.level*9.11
		self.power=69+(self.level-1)*42
		self.name ="Meme"
		# self.compute_rewards()
class WindElemental(Elemental):
	def __init__(self,level):
		super(WindElemental,self).__init__(level)
		self.modif=[mod.Camphoric, mod.Dank, mod.Destructive, mod.Dusty, mod.Forgotten, mod.Lightning, mod.Nasty]
		self.max_health=5+self.level*15
		self.health=5+self.level*15
		self.power=11+(self.level-1)*14
		self.name="Wind Elemental"
		# self.compute_rewards()

class WaterElemental(Elemental):
	def __init__(self,level):
		super(WaterElemental,self).__init__(level)
		self.modif=[mod.Destructive, mod.Forgotten, mod.Funky, mod.Foul, mod.Musky, mod.Nasty, mod.Putrid, mod.Weak]
		self.power=4+(self.level-1)*20
		self.name="Water Elemental"
		# self.compute_rewards()

class FireElemental(Elemental):
	def __init__(self,level):
		super(FireElemental,self).__init__(level)
		self.modif=[mod.Scorched, mod.Dank]
		self.max_health=10+self.level*20
		self.health=10+self.level*20
		self.power=18+(self.level-1)*20
		self.name="Fire Elemental"
		# self.compute_rewards()


class EarthElemental(Elemental):
	def __init__(self,level):
		super(EarthElemental,self).__init__(level)
		self.modif=[mod.Acidic, mod.Caustic, mod.Decaying, mod.Destructive, mod.Dieing, mod.Flowery, mod.Forgotten, mod.Foul, mod.Musky, mod.Nasty, mod.Normal, mod.Rancid, mod.Scorched]
		self.max_health=100+self.level*30
		self.health=100+self.level*30
		self.power=4+(self.level-1)*12
		self.name="Earth Elemental"
		# self.compute_rewards()

class Demigod(Monster):
	def __init__(self,level):
		super(Demigod,self).__init__(level)
		self.modif=[mod.Camphoric, mod.Dank, mod.Destructive, mod.Forgotten, mod.Funky, mod.Lightning, mod.Nasty]
		self.multiplier=1.6
		self.max_health=100+self.level*18
		self.health=100+self.level*18
		self.power=20+(self.level-1)*14
		self.action_points=2
		self.name="Demigod"
		# self.compute_rewards()

class Overcharger(Monster):
	def __init__(self,level):
		super(Overcharger,self).__init__(level)
		self.modif=[mod.Dank, mod.Destructive, mod.Forgotten, mod.Funky, mod.Lightning, mod.Nasty]
		self.multiplier=1.05
		self.max_health=5+self.level*10
		self.health=5+self.level*10
		self.power=30+(self.level-1)*65
		self.ap=1
		self.action_points=1
		self.name="Overcharger"
		# self.compute_rewards()

class Cyclops(Monster):
	def __init__(self,level):
		super(Cyclops,self).__init__(level)
		self.modif=[mod.Tiny, mod.Camphoric, mod.Caustic, mod.Dank, mod.Destructive, mod.Dieing, mod.Forgotten, mod.Lowly, mod.Musky, mod.Nasty, mod.Normal, mod.Weak]
		self.max_health=60+self.level*20
		self.health=60+self.level*20
		self.power=6+(self.level-1)*16
		self.name="Cyclops"
		# self.compute_rewards()


MONSTERLIST = {
	Skeleton:{
		'probability':20.0,
		'groupsize':3
	},
	Goblin:{
		'probability':15.0,
		'groupsize':6
	},
	Spider:{
		'probability':25.0,
		'groupsize':12
	},
	Assassin:{
		'probability':2.0,
		'groupsize':1
	},
	Hidden_Devourer:{
		'probability':3.0,
		'groupsize':1
	},
	Ogre:{
		'probability':10.0,
		'groupsize':2
	},
	Hellhound:{
		'probability':2.0,
		'groupsize':2
	},
	Sorcerer:{
		'probability':3.0,
		'groupsize':1
	},
	Meme:{
		'probability':.1,
		'groupsize':3
	},
	WindElemental:{
		'probability':8.0,
		'groupsize':4
	},
	WaterElemental:{
		'probability':6.0,
		'groupsize':3
	},
	FireElemental:{
		'probability':3.0,
		'groupsize':3
	},
	EarthElemental:{
		'probability':3.0,
		'groupsize':2
	},
	Demigod:{
		'probability':.5,
		'groupsize':1
	},
	Overcharger:{
		'probability':2.0,
		'groupsize':2
	},
	Cyclops:{
		'probability':4.0,
		'groupsize':3
	}
}
