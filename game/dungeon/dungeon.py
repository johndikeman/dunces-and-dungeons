class Dungeon(object):
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

	def handle_monster_turn(self):
		pass


class Room:
	def __init__(self,containing_dungeon):
		self.containing_dungeon = containing_dungeon
		self.neighbors = []
		# the room should only be 50% weaker than the dungeon level or 150% stronger- this is not a mistake
		self.level = ceil((random.random() + .5) * containing_dungeon.level)

	# def examine(self,examiner):
	# 	if examiner.perception > 