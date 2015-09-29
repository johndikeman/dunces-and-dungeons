import math, random, base
import entity.monster.monsters as monsters

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
		self.roomslist=""
		self.starting_room = Room(self,self.party)
		self.starting_room.test = 0
		self.rooms = []
		self.roomsmap=[]
		
		self.size = size
		self.room_num = 1
		# okso current_room is only used in generation. to access the ACTIVE room, use self.active_room instead.

		current_room = self.starting_room

		for a in range(size):
			row = []
			for b in range(size):
				row.append(None)
			self.rooms.append(row)
		for a in range(size):
			row = []
			for b in range(size):
				row.append('F')
			self.roomsmap.append(row)


		self.starting_room.cords = (0,0)
		self.rooms[0][0] = self.starting_room
		self.rooms[0][0].generate()

			

	def handle_monster_turn(self):
		self.active_room.handle_monster_turn()

	def start(self):
		print 'you find yourself in a large, spooky dungeon.'
		self.active_room = self.starting_room
		self.active_room.enter()

	def to_str(self):
		ret = ''
		for a in self.rooms:
			for b in a:
				if isinstance(b,Room):
					ret += 'ROOM '
				else:
					ret += '____ ' 
			ret += '\n'
		return ret

class Hub(Dungeon):
	def __init__(self,party):
		self.shop = []
		self.party = party

	def enter_shop(self):
		print 'there is nothing here yet!'

	def leave_dungeon(self):
		he = [10,20,30,50]
		ind = base.make_choice(['smol','medium','large','goliath'],'size')
		self.party.current_dungeon = Dungeon(he[ind],self.party.get_avg_level(),self.party)
		self.party.current_dungeon.start()
		print self.party.current_dungeon


	def start(self):
		print 'welcome to the hub!'


class Room(object):
	def __init__(self,containing_dungeon,party):
		self.containing_dungeon = containing_dungeon
		self.neighbors = []
		# the room should only be 50% weaker than the dungeon level or 150% stronger- this is not a mistake
		self.level = math.ceil((random.random() + .5) * containing_dungeon.level)
		self.description = "a %s smelling room, with %s and %s walls and a %s floor." % (random.choice(SMELL),random.choice(TOUCH),random.choice(TOUCH),random.choice(TOUCH))
		# this is to test the generation
		self.test = -9999

		# this will identify the rooms to the players for now
		self.id = random.getrandbits(32)
		self.things = base.Inventory(self)
		self.identified_things = base.Inventory(self)

		self.party = party

		self.cords = None

		self.directions = {'north':(-1,0),'south':(1,0),'east':(0,1),'west':(0,-1)}

	def generate(self):
		for monstar in monsters.spawn(self.level):
			self.things.append(monstar)
		for direction, dircords in self.directions.iteritems():
			x,y = dircords
			selfx,selfy = self.cords

			newx = x + selfx
			newy = y + selfy
			ma = self.containing_dungeon.size

			if newx >= 0 and newx < ma and newy >=0 and newy < ma and not self.containing_dungeon.rooms[newx][newy]:
				if len(self.get_neighbors().keys()) <= 1:
					self.generate_neighbor(direction)
				else:
					if len(self.get_neighbors().keys()) < 3 and base.D6.roll() > 4:
						self.generate_neighbor(direction)

	def get_neighbors(self):
		# this returns a dictionary structured like {'direction':room_object}
		neighbors = {}

		for direction, coordpair in self.directions.iteritems():
			x,y = coordpair
			try:
				newx,newy = self.cords[0]+x,self.cords[1]+y
				if newx >=0 and newy >=0:
					if self.containing_dungeon.rooms[newx][newy]:
						neighbors.update({direction:self.containing_dungeon.rooms[self.cords[0]+x][self.cords[1]+y]})
			except IndexError:
				pass
		return neighbors


	def generate_neighbor(self,di):
		# print 'generating n to the %s at %s' % (di,str(self.cords))
		new_room = Room(self.containing_dungeon,self.party)
		x,y = self.cords

		dirx,diry = self.directions[di]
		new_room.cords = (x+dirx,y+diry)
		self.containing_dungeon.roomslist+=''+str(x+dirx)+' '+str(y+diry)+' '
		self.containing_dungeon.rooms[new_room.cords[0]][new_room.cords[1]] = new_room
		self.containing_dungeon.rooms[new_room.cords[0]][new_room.cords[1]].generate()

	def to_str(self):
		# this method was a thing at one point, but now it is not. rip
		return self.description

	def move_to(self,ind):
<<<<<<< HEAD
		
=======
>>>>>>> origin/master
		self.containing_dungeon.active_room = self.get_neighbors()[self.get_neighbors().keys()[ind]]
		self.containing_dungeon.active_room.enter()
		
		##HELP! i need to put all possible neighbors adjacent to a room already in to be ? 
		

	def enter(self):
		self.party.current_dungeon.roomsmap[self.cords[0]][self.cords[1]]='T'
		g=self.cords[0]
		h=self.cords[1]
		if((str(g+1)+' '+str(h)) in self.containing_dungeon.roomslist and self.party.current_dungeon.roomsmap[g+1][h]!="T"):
			self.party.current_dungeon.roomsmap[g+1][h]='?'
		if((str(g-1)+' '+str(h)) in self.containing_dungeon.roomslist and self.party.current_dungeon.roomsmap[g-1][h]!="T"):
			self.party.current_dungeon.roomsmap[g-1][h]='?'
		if((str(g)+' '+str(h+1)) in self.containing_dungeon.roomslist and self.party.current_dungeon.roomsmap[g][h+1]!="T"):
			self.party.current_dungeon.roomsmap[g][h+1]='?'
		if((str(g)+' '+str(h-1)) in self.containing_dungeon.roomslist and self.party.current_dungeon.roomsmap[g][h-1]!="T"):
			self.party.current_dungeon.roomsmap[g][h-1]='?'
		print 'you enter a %s, CORDS:%s' % (self.description,str(self.cords))

	def handle_monster_turn(self):
		for thing in self.things:
			if thing.alive:
				thing.do_turn()


		