import math, random, base

class Dungeon(object):
	def __init__(self, size, level, party):
		# as far as i can tell, the generation algorithm doesn't pay attention to the size
		# parameter and just does what it feels like. this is probably a bug.
		num_doors = 0
		self.level = level
		self.party = party

		self.starting_room = Room(self)
		self.starting_room.test = 0
		current_room = self.starting_room

		for a in range(0,size):
			if num_doors < 2:
				if base.D6.roll() <= 3:
					current_room.generate_neighbor()
					num_doors += 1
			else:
				#generate neighbor needs to return the Room that it generates
				current_room = current_room.generate_neighbor()
				num_doors = 0

	def handle_monster_turn(self):
		pass

	def start(self):
		print 'you find yourself in a large, spooky dungeon.'
		self.active_room = self.starting_room


class Room(object):
	def __init__(self,containing_dungeon):
		self.containing_dungeon = containing_dungeon
		self.neighbors = []
		# the room should only be 50% weaker than the dungeon level or 150% stronger- this is not a mistake
		self.level = math.ceil((random.random() + .5) * containing_dungeon.level)

		# this is to test the generation
		self.test = -9999

		# this will identify the rooms to the players for now
		self.id = random.getrandbits(32)

	def generate_neighbor(self):
		new_room = Room(self.containing_dungeon)
		new_room.id = self.id + 1
		self.neighbors.append(new_room)
		new_room.neighbors.append(self)

		return new_room
	# def examine(self,examiner):
	# 	if examiner.perception > 

	def to_str(self):
		# this method was a thing at one point, but now it is not. rip
		pass
		