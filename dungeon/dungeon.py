import math, random, base
import entity.monster.monsters as monsters
import entity.item.items as items
import entity.chest as chesteses
import os.path
import entity.thing as thing
import entity.item.consumable as consumable
import entity.item.controller as control
import entity.monster.bosses as boss


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
		self.gold_reward = (self.level * 100) * self.size
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

		temp = []
		for a in self.rooms:
			for b in a:
				if b:
					temp.append(b)
		final = random.choice(temp)
		# final = temp[0]
		final.things.append(LeaveOption())

		final.things.append(random.choice(boss.boss_options)(final.level))

		# self.rooms[0][0].things.append(LeaveOption())

	def leave_dungeon(self):
		self.party.current_dungeon = self.party.hub
		self.party.current_dungeon.start()

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
		#self.shop = []
		self.party = party
		self.shop = {
			"health":[consumable.HealthPotion() for a in self.party.inventory],
			"weapons":[],
			"armor":[],
			"spells":[], # potions for errybody
			"utility":[]
		}


	def enter_shop(self):
		print 'you have %d gold!' % (self.party.inventory[self.party.index].gold)
		shopping = base.make_choice(self.shop.keys(),'category')
		item = base.make_choice( ['%s for %d' % (a.to_str(),a.get_cost()) for a in self.shop[self.shop.keys()[shopping]]],'item',True)
		if(item is None):
			print 'You bought nothing!'
		else:
			item_object = self.shop[self.shop.keys()[shopping]][item]
			# remove the item from the shop afterwards
			# self.shop[self.shop.keys()[shopping]].remove(item_object)
			success = self.party.inventory[self.party.index].buy_item(item_object)
			if success:
				self.shop[self.shop.keys()[shopping]].remove(item_object)
				print 'successfully purchased a %s' % item_object.to_str()
			# inventory.append(item_object)
			# self.party.inventory[self.party.index].gold -= item_object.cost
		# allow the player to shop as much as they want in a turn
		if raw_input('continue? (y/n) ') is 'y':
			self.enter_shop()


	def leave_dungeon(self):
		he = [5,8,15,25]
		ind = base.make_choice(['smol','medium','large','goliath'],'size')
		self.party.current_dungeon = Dungeon(he[ind],self.party.get_avg_level(),self.party)
		for a in self.party.inventory:
			a.action_points=a.base_ap
		self.party.current_dungeon.start()
		# print self.party.current_dungeon

	def save_game(self):
		print 'Name your save file'
		ans=raw_input()
		f=open(ans+'.txt','w')
		f.write(str(len(self.party.inventory))+'\n')
		for currentplayer in self.party.inventory:
			f.write(currentplayer.name+'\n')
			#f.write(str(currentplayer.party)+'\n')
			f.write(str(currentplayer.action_points)+'\n')
			f.write(str(currentplayer.base_ap)+'\n')
			f.write(str(currentplayer.options)+'\n')
			f.write(str(currentplayer.alive)+'\n')
			f.write(str(currentplayer.race)+'\n')
			f.write(str(currentplayer.health)+'\n')
			f.write(str(currentplayer.max_health)+'\n')
			f.write(str(currentplayer.armor)+'\n')
			f.write(str(currentplayer.gold)+'\n')
			for disitem in currentplayer.inventory:
				f.write(str(disitem)+'\n')
			f.write(str(currentplayer.equipment)+'\n\n\n\n')
	def handle_monster_turn(self):
		pass

	def start(self):
		controller = control.ItemController(self.party.get_avg_level())
		for category in self.shop.keys():
			for b in range(random.randint(len(self.party.inventory),len(self.party.inventory)+5)):
				inst = controller.generate(category)
				if inst:
					self.shop[category].append(inst)
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
		# self.identified_things = base.Inventory(self)

		self.party = party

		self.cords = None

		self.directions = {'north':(-1,0),'south':(1,0),'east':(0,1),'west':(0,-1)}

	def generate(self):
		for monstar in monsters.spawn(self.level):
			self.things.append(monstar)

		chest = chesteses.spawn(self.level)
		if chest:
			self.things.append(chest)

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
		self.containing_dungeon.active_room = self.get_neighbors()[self.get_neighbors().keys()[ind]]
		self.containing_dungeon.active_room.enter()

		##HELP! i need to put all possible neighbors adjacent to a room already in to be ?


	def enter(self):
		for a in self.things:
			if(isinstance(a,LeaveOption) ):
				self.party.current_dungeon.roomsmap[self.cords[0]][self.cords[1]]='E'
			else:
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
		# print 'you enter a %s, CORDS:%s' % (self.description,str(self.cords))

	def handle_monster_turn(self):
		# print "THINGS: %s" % str(self.things)
		# print 'ID: %s' % str(self.identified_things)
		for thing in self.things:
			thing.action_points = thing.base_ap
			while thing.alive and thing.action_points > 0:
				thing.do_turn()
		# for thing in self.identified_things:
		# 	if thing.alive:
		# 		thing.do_turn()




class LeaveOption(thing.InteractiveObject):
	def __init__(self):
		super(LeaveOption,self).__init__()
		self.options = ['leave the dungeon']

	def do_turn(self,arg):
		if arg == self.options[0]:
			if len(self.owner.things) == 1:
				for player in self.owner.containing_dungeon.party.inventory:
					player.gold += (self.owner.containing_dungeon.gold_reward / 5)
				print 'each player is awarded %d gold!' % (self.owner.containing_dungeon.gold_reward / 5)

				self.owner.containing_dungeon.leave_dungeon()
			else:
				print 'you can\'t leave the dungeon while you\'re under attack!'

	def to_str(self):
		return 'a ladder out of the dungeon'
