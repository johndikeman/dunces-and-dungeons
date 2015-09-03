import random

D6 = Die(6)
D6 = Die(12)
D6 = Die(20)
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
	pass

class Player(Entity):
	pass

class Party:
	pass

class Room:
	def __init__(self,containing_dungeon):
		self.containing_dungeon = containing_dungeon
		self.neighbors = []
		self.level = ceil((random.random() + .5) * containing_dungeon.level)

	def examine(self,examiner):
		if examiner.perception > 


class Monster(Entity):
	pass
class Skeleton(Monster)
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

class WireTrap:
	def __init__(self,damage):
		pass

class Die:
	def __init__(self,num):
		self.num = num
	
	def roll():
		return random.randint(1,self.num)
