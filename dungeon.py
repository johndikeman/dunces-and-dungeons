import random

D6 = Die(6)
D12 = Die(12)
D20 = Die(20)
# Im working here shhh

class Dungeon:
	def __init__(self, size, level, party):
		starting_room = Room()
		current_room = starting_room
		num_doors = 0
		self.level = level
		self.party = party

		for a in range(0,size):
			if num_doors < 2:
				if D6.roll() <= 3:
					current_room.generate_neighbor()
					num_doors += 1
			else:
				#generate neighbor needs to return the Room that it generates
				current_room = current_room.generate_neighbor()
				num_doors = 0


class Entity:
	def __init__(self):
		# not sure about this
		# attack_range = 0
		self.strength = 0
		self.perception = 0
		self.luck = 0
		self.agility = 0
		self.mana = 0
		self.health = 0

	def do_turn(self):
		pass

	def kill(self):
		self.alive = False

class Player(Entity):
	pass

class Party:
	pass

class Room:
	def __init__(self,containing_dungeon):
		self.containing_dungeon = containing_dungeon
		self.neighbors = []
		# the room should only be 50% weaker than the dungeon level or 150% stronger- this is not a mistake
		self.level = ceil((random.random() + .5) * containing_dungeon.level)

	def examine(self,examiner):
		if examiner.perception > 


class Monster(Entity):
	def __init__(self):
		self.agro= None

class Skeleton(Monster):
	pass

class Item(Entity):
	def __init__(self):
		pass
	def examine(self, examiner):
	 	pass

# this is a superclass for general traps
class Trap:
	def __init__(self):
		pass
	def is_triggered():
		pass
	def trigger():
		pass
	def warn():
		return "there could be a trap around here."
	def detect():
		return "you spy a trap!"

class WireTrap(Trap):
	def __init__(self,damage):
		pass

class Die:
	def __init__(self,num):
		self.num = num
	
	def roll():
		return random.randint(1,self.num)
