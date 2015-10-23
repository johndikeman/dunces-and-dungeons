import base, random, time
import status.player_statuses as s

class ModifyMons(object):
	def __init__(self):
		pass
		
	def do_turn(self):
		pass

	def to_str(self):
		return "Modified"

class Acidic(ModifyMons):
	def __init__(self,monster):
		monster.health*=.5
		monster.power*=1.1

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance > 10:
			target.statuses.append(s.Poison(3,(chance*self.level-10*self.level)/4))
			print target.name +"has been poisoned by" + self.name

	def to_str(self):
		return "Acidic"

class Camphoric(ModifyMons):
	def __init__(self,monster):
		monster.health*=.5
		monster.power*=2
		monster.ap+=1

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Camphoric"

class Caustic(ModifyMons):
	def __init__(self,monster):
		monster.health*=.5

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>16:
			target.stasuses.append(s.Poison(2,self.level*base.D2.roll()))
			print target.name + " has been poisoned by "+self.name

	def to_str(self):
		return "Caustic"

class Dank(ModifyMons):
	def __init__(self,monster):
		monster.health*=1.5
		monster.power*=2
		monster.ap+=2

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance > 18:
			target.stasuses.append(s.Stun(base.D2.roll()))
			print target.name +" has been stunned by " + self.name
		chance2=base.D20.roll()
		if chance2 > 19:
			target.stasuses.append(s.Poison(base.D4.roll(),base.D6.roll()*self.level))
			print target.name +" has been poisoned by " + self.name
		chance3=base.D20.roll()
		if chance3>18:
			target.stasuses.append(s.Burn(base.D6.roll(),self.level*base.D2.roll()))
			print target.name + " has been burned by "+self.name

	def to_str(self):
		return "Dank"

class Decaying(ModifyMons):
	def __init__(self,monster):
		monster.health*=.3
		monster.power*=.5
		monster.ap+=1

	def do_turn(self,target):
		self.health-=10;

	def to_str(self):
		return "Decaying"

class Destructive(ModifyMons):
	def __init__(self,monster):
		monster.health*=1.2
		monster.power*=3

	def do_turn(self,target):
		chance = base.D20.roll()
		if chance>19:
			target.stasuses.append(s.Stun(base.D6.roll()))
			print target.name + " has been stunned by "+self.name

	def to_str(self):
		return "Destructive"
	
class Dieing(ModifyMons):
	def __init__(self,monster):
		monster.health*=.05
		monster.power*=.05

	def do_turn(self,target):
		self.health-=5;

	def to_str(self):
		return "Dieing"

class Dusty(ModifyMons):
	def __init__(self,monster):
		monster.health*=.7
		monster.power*=.5

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>19:
			target.stasuses.append(s.Poison(base.D2.roll(),3))
			print target.name + " has been poisoned by "+self.name

	def to_str(self):
		return "Dusty"

class Fetid(ModifyMons):
	def __init__(self,monster):
		monster.health*=.2
		monster.power*=.5

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Fetid"

class Flowery(ModifyMons):
	def __init__(self,monster):
		monster.health=1
		monster.power=1

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>19:
			target.stasuses.append(s.Healing())
			print target.name + " has been healed by "+self.name

	def to_str(self):
		return "Flowery"

class Forgotten(ModifyMons):
	def __init__(self,monster):
		monster.health*=1.1
		monster.power*=.5

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Forgotten"

class Foul(ModifyMons):
	def __init__(self,monster):
		monster.health*=.8
		monster.power-=12

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>16:
			target.stasuses.append(s.Poison(2,self.level*base.D2.roll()))
			print target.name + " has been poisoned by "+self.name

	def to_str(self):
		return "Foul"

class Funky(ModifyMons):
	def __init__(self,monster):
		monster.health+=random.randint(1,150)
		monster.power*=random.randint(1,4)
		monster.ap+=1

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Funky"

class Lightning(ModifyMons):
	def __init__(self,monster):
		monster.health*=.1
		monster.power*=3
		monster.ap*=2

	def do_turn(self,target):
		chance =base.D20.roll()
		if chance > 12:
			self.ap+=1
			print self.name+" can attack again!"

	def to_str(self):
		return "Lightning"

class Lowly(ModifyMons):
	def __init__(self,monster):
		monster.health*=.4
		monster.power*=.5
		monster.ap=1

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Lowly"

class Musky(ModifyMons):
	def __init__(self,monster):
		monster.health*=2
		monster.power*=1.2
		monster.ap+=2

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>19:
			target.stasuses.append(s.Stun(base.D3.roll()))
			print target.name + " has been stunned by "+self.name

	def to_str(self):
		return "Musky"

class Nasty(ModifyMons):
	def __init__(self,monster):
		monster.health*=.9
		monster.power*=1.2
		monster.ap*=2

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>12:
			target.stasuses.append(s.Stun(2))
			print target.name + " has been stunned by "+self.name

	def to_str(self):
		return "Nasty"

class Normal(ModifyMons):
	def __init__(self,monster):
		pass

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Normal"

class Putrid(ModifyMons):
	def __init__(self,monster):
		monster.health*=.6
		monster.power*=.1

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Putrid"

class Rancid(ModifyMons):
	def __init__(self,monster):
		monster.health-=20
		monster.power*=3
		monster.ap*=2

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>16:
			target.stasuses.append(s.Poison(2,self.level*base.D2.roll()))
			print target.name + " has been poisoned by "+self.name

	def to_str(self):
		return "Rancid"

class Scorched(ModifyMons):
	def __init__(self,monster):
		monster.health*=.4
		monster.power*=.5

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>14:
			target.stasuses.append(s.Poison(1,self.level*base.D3.roll()))
			print target.name + " has been burned by "+self.name

	def to_str(self):
		return "Scorched"

class Tiny(ModifyMons):
	def __init__(self,monster):
		monster.health*=.3
		monster.power*=.3

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Tiny"

class Weak(ModifyMons):
	def __init__(self,monster):
		monster.health*=.1
		monster.power*=.2

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Weak"