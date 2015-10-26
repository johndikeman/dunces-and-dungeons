import base, random, time
import entity.status.player_statuses as s

class ModifyMons(base.Entity):
	def __init__(self):
		super(ModifyMons,self).__init__()

	def do_turn(self):
		pass

	def to_str(self):
		return "Modified"

# hey altering just the ap variable only gives them the extra for one turn,
# cause it gets reset to base_ap. im not sure that this was your intent

# these should inherit their constructors from the superclass? right? right?
class Acidic(ModifyMons):
	def apply(self):
		self.owner.health*=.5
		self.owner.power*=1.1

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance > 10:
			target.statuses.append(s.Poison(3,(chance*self.level-10*self.level)/4))
			print target.name +"has been poisoned by" + self.name

	def to_str(self):
		return "Acidic"

class Camphoric(ModifyMons):
	def apply(self):
		self.owner.health*=.5
		self.owner.power*=2
		self.owner.ap+=1

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Camphoric"

class Caustic(ModifyMons):
	def apply(self):
		self.owner.health*=.5

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>16:
			target.stasuses.append(s.Poison(2,self.level*base.D2.roll()))
			print target.name + " has been poisoned by "+self.name

	def to_str(self):
		return "Caustic"

class Dank(ModifyMons):
	def apply(self):
		self.owner.health*=1.5
		self.owner.power*=2
		self.owner.ap+=2

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
	def apply(self):
		self.owner.health*=.3
		self.owner.power*=.5
		self.owner.ap+=1

	def do_turn(self,target):
		self.health-=10;

	def to_str(self):
		return "Decaying"

class Destructive(ModifyMons):
	def apply(self):
		self.owner.health*=1.2
		self.owner.power*=3

	def do_turn(self,target):
		chance = base.D20.roll()
		if chance>19:
			target.stasuses.append(s.Stun(base.D6.roll()))
			print target.name + " has been stunned by "+self.name

	def to_str(self):
		return "Destructive"

class Dieing(ModifyMons):
	def apply(self):
		self.owner.health*=.05
		self.owner.power*=.05

	def do_turn(self,target):
		self.health-=5;

	def to_str(self):
		return "Dieing"

class Dusty(ModifyMons):
	def apply(self):
		self.owner.health*=.7
		self.owner.power*=.5

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>19:
			target.stasuses.append(s.Poison(base.D2.roll(),3))
			print target.name + " has been poisoned by "+self.name

	def to_str(self):
		return "Dusty"

class Fetid(ModifyMons):
	def apply(self):
		self.owner.health*=.2
		self.owner.power*=.5

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Fetid"

class Flowery(ModifyMons):
	def apply(self):
		self.owner.health=1
		self.owner.power=1

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>19:
			target.stasuses.append(s.Healing())
			print target.name + " has been healed by "+self.name

	def to_str(self):
		return "Flowery"

class Forgotten(ModifyMons):
	def apply(self):
		self.owner.health*=1.1
		self.owner.power*=.5

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Forgotten"

class Foul(ModifyMons):
	def apply(self):
		self.owner.health*=.8
		self.owner.power-=12

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>16:
			target.stasuses.append(s.Poison(2,self.level*base.D2.roll()))
			print target.name + " has been poisoned by "+self.name

	def to_str(self):
		return "Foul"

class Funky(ModifyMons):
	def apply(self):
		self.owner.health+=random.randint(1,150)
		self.owner.power*=random.randint(1,4)
		self.owner.ap+=1

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Funky"

class Lightning(ModifyMons):
	def apply(self):
		self.owner.health*=.1
		self.owner.power*=3
		self.owner.ap*=2

	def do_turn(self,target):
		chance =base.D20.roll()
		if chance > 12:
			self.ap+=1
			print self.name+" can attack again!"

	def to_str(self):
		return "Lightning"

class Lowly(ModifyMons):
	def apply(self):
		self.owner.health*=.4
		self.owner.power*=.5
		self.owner.ap=1

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Lowly"

class Musky(ModifyMons):
	def apply(self):
		self.owner.health*=2
		self.owner.power*=1.2
		self.owner.ap+=2

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>19:
			target.stasuses.append(s.Stun(base.D3.roll()))
			print target.name + " has been stunned by "+self.name

	def to_str(self):
		return "Musky"

class Nasty(ModifyMons):
	def apply(self):
		self.owner.health*=.9
		self.owner.power*=1.2
		self.owner.ap*=2

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>12:
			target.stasuses.append(s.Stun(2))
			print target.name + " has been stunned by "+self.name

	def to_str(self):
		return "Nasty"

class Normal(ModifyMons):
	def apply(self):
		pass

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Normal"

class Putrid(ModifyMons):
	def apply(self):
		self.owner.health*=.6
		self.owner.power*=.1

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Putrid"

class Rancid(ModifyMons):
	def apply(self):
		self.owner.health-=20
		self.owner.power*=3
		self.owner.ap*=2

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>16:
			target.stasuses.append(s.Poison(2,self.level*base.D2.roll()))
			print target.name + " has been poisoned by "+self.name

	def to_str(self):
		return "Rancid"

class Scorched(ModifyMons):
	def apply(self):
		self.owner.health*=.4
		self.owner.power*=.5

	def do_turn(self,target):
		chance=base.D20.roll()
		if chance>14:
			target.stasuses.append(s.Poison(1,self.level*base.D3.roll()))
			print target.name + " has been burned by "+self.name

	def to_str(self):
		return "Scorched"

class Tiny(ModifyMons):
	def apply(self):
		self.owner.health*=.3
		self.owner.power*=.3

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Tiny"

class Weak(ModifyMons):
	def apply(self):
		self.owner.health*=.1
		self.owner.power*=.2

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Weak"
