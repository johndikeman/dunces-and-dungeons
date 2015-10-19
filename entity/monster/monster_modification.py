import base, random, time

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
		pass
		#need to instantiate a poison that is based on the monsters level.

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
		pass

	def to_str(self):
		return "Caustic"

class Dank(ModifyMons):
	def __init__(self,monster):
		monster.health*=1.5
		monster.power*=2
		monster.ap+=2

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Dank"

class Decaying(ModifyMons):
	def __init__(self,monster):
		monster.health*=.3
		monster.power*=.5
		monster.ap+=1

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Decaying"

class Destructive(ModifyMons):
	def __init__(self,monster):
		monster.health*=1.2
		monster.power*=3

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Destructive"
	
class Dieing(ModifyMons):
	def __init__(self,monster):
		monster.health*=.05
		monster.power*=.05

	def do_turn(self,target):
		pass

	def to_str(self):
		return "Dieing"

class Dusty(ModifyMons):
	def __init__(self,monster):
		monster.health*=.7
		monster.power*=.5

	def do_turn(self,target):
		pass

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
		pass

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
		pass

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
		pass

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
		pass

	def to_str(self):
		return "Musky"

class Nasty(ModifyMons):
	def __init__(self,monster):
		monster.health*=.9
		monster.power*=1.2
		monster.ap*=2

	def do_turn(self,target):
		pass

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
		pass

	def to_str(self):
		return "Rancid"

class Scorched(ModifyMons):
	def __init__(self,monster):
		monster.health*=.4
		monster.power*=.5

	def do_turn(self,target):
		pass

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