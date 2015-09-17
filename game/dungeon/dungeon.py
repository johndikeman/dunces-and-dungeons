import math, random, base

# these words are from http://acreativemoment.com/2008/07/18/words-to-describe-smell-sound-taste-touch/
# feel free to add some more that you don't see
SMELL = ('acidic acrid aromatic camphoric fetid flowery foul fragrant fresh funky heady musky musty nasty noxious perfumed piney pungent rancid savory sharp smelly stinky stuffy sweet'.split(' '))
TOUCH = ('tough bristly burning cold cottony damp dank moist dry feathery frosty furry fuzzy gnarled hairy hot knobbed knotted leathery limp lumpy oily puffy ribbed rough rubbery sandy sharp slimy smooth sticky velvety wet'.split(' '))

class Dungeon(object):
	def __init__(self, size, level, party):
		# as far as i can tell, the generation algorithm doesn't pay attention to the size
		# parameter and just does what it feels like. this is probably a bug.
		num_doors = 0
		self.level = level
		self.party = party
		self.active_room = None
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
		self.active_room.handle_monster_turn()

	def start(self):
		print 'you find yourself in a large, spooky dungeon.'
		self.active_room = self.starting_room
		self.active_room.enter()


class Room(object):
	def __init__(self,containing_dungeon):
		self.containing_dungeon = containing_dungeon
		self.neighbors = []
		# the room should only be 50% weaker than the dungeon level or 150% stronger- this is not a mistake
		self.level = math.ceil((random.random() + .5) * containing_dungeon.level)
		self.description = "a %s smelling room, with %s and %s walls and a %s floor." % (random.choice(SMELL),random.choice(TOUCH),random.choice(TOUCH),random.choice(TOUCH))
		# this is to test the generation
		self.test = -9999

		# this will identify the rooms to the players for now
		self.id = random.getrandbits(32)
		self.contents = Inventory()

	def generate_neighbor(self):
		new_room = Room(self.containing_dungeon)
		# each room is assigned a unique ID at generation
		new_room.id = self.id + len(self.neighbors) + 1
		self.neighbors.append(new_room)
		new_room.neighbors.append(self)

		return new_room
	# def examine(self,examiner):
	# 	if examiner.perception > 

	def to_str(self):
		# this method was a thing at one point, but now it is not. rip
		return 'this is a room, id %s' % str(self.id)

	def move_to(self,ind):
		self.containing_dungeon.active_room = self.neighbors[ind]
		self.neighbors[ind].enter()

	def enter(self):
		print 'you enter a %s' % self.description

	def handle_monster_turn(self):
		for thing in self.things:
			thing.do_turn()


		