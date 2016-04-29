import math, random, base
import entity.monster.monsters as monsters
import entity.item.items as items
import entity.chest as chesteses
import os.path
import entity.thing as thing
import entity.item.consumable as consumable
import entity.item.controller as control
import entity.monster.bosses as boss
import entity.item.utils as utils


# these words are from http://acreativemoment.com/2008/07/18/words-to-describe-smell-sound-taste-touch/
# feel free to add some more that you don't see
SMELL = ('acidic acrid aromatic camphoric fetid flowery foul fragrant fresh funky heady musky musty nasty noxious perfumed piney pungent rancid savory sharp smelly stinky stuffy sweet'.split(' '))
TOUCH = ('tough bristly burning cold cottony damp dank moist dry feathery frosty furry fuzzy gnarled hairy hot knobbed knotted leathery limp lumpy oily puffy ribbed rough rubbery sandy sharp slimy smooth sticky velvety wet'.split(' '))



class Dungeon(object):
	def __init__(self, size, level, party):
		""" size: int, the sqrt of the number of rooms in the dungeon
			level: int, the level of the dungeon. this affects the level of the monsters and stuff.
			party: entity.player.players.Party object
		"""

		# as far as i can tell, the generation algorithm doesn't pay attention to the size
		# parameter and just does what it feels like. this is probably a bug.
		num_doors = 0
		# this is the level of the dungeon. it affects the strength of the monsters
		self.level = level
		self.party = party
		self.active_room = None
		self.roomslist=""
		self.starting_room = Room(self,self.party)
		self.starting_room.test = 0
		self.rooms = []
		self.things =[]
		self.roomsmap=[]
		self.directions = {'north':(-1,0),'south':(1,0),'east':(0,1),'west':(0,-1)}

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

		current_x, current_y = (0,0)
		self.starting_room.cords = (0,0)
		self.rooms[0][0] = self.starting_room
		needed = self.rooms[0][0].generate()
		cornerlist = {(0,0):('south','east')}

		for a in range(int(self.size / 2)):
			corner_x, corner_y = random.choice(cornerlist.keys())
			print cornerlist
			dx, dy = self.directions[random.choice(cornerlist[(corner_x,corner_y)])]
			current_x, current_y = corner_x, corner_y
			while dx + current_x >= 0 and dx + current_x < self.size and \
				dy + current_y >= 0 and dy + current_y < self.size:
				if base.D100.roll() <= 15:
					self.rooms[current_x + dx][current_y + dy] = Room(self,self.party)
					self.rooms[current_x + dx][current_y + dy].cords = (current_x + dx, current_y + dy)
					self.rooms[current_x + dx][current_y + dy].generate()
					current_x, current_y = (current_x + dx,current_y + dy)
				else:
					open_directions = self.rooms[current_x][current_y].get_open_spaces()
					for ind, a in enumerate(open_directions):
						if self.directions[a] == (dx,dy):
							open_directions = open_directions[:ind] + open_directions[ind+1:]

					cornerlist.update({(current_x,current_y):open_directions})




		temp = []
		for a in self.rooms:
			for b in a:
				if b:
					temp.append(b)

		# grab a random room to serve as the boss room
		final = random.choice(temp)
		# final = temp[0]
		final.things.append(LeaveOption())

		final.things.append(random.choice(boss.boss_options)(final.level))

		# self.rooms[0][0].things.append(LeaveOption())

	def leave_dungeon(self):
		"""this method is called when the dungeon is completed."""
		# # destroy any maps in the inventory
		# for a in self.party.inventory:
		# 	if a.inventory.contains_type(utils.CompletedMap):
		# 		print "%s's map crumbles to dust" % a.name
		# 		a.inventory.remove(utils.CompletedMap)
		# set the current dungeon back to the hub
		self.party.current_dungeon = self.party.hub
		self.party.current_dungeon.start()

	def handle_monster_turn(self):
		self.active_room.handle_monster_turn()

	def start(self):
		base.put('you find yourself in a large, spooky dungeon.')
		self.active_room = self.starting_room
		self.active_room.enter()

	def to_str(self):
		tmap = []
		for a in range(self.size):
			tmap.append([])
			for b in range(self.size):
				tmap[b].append(None)

		rooms = self.rooms
		for row in range(len(rooms)):
			for col in range(len(rooms[row])):
				# check first if there is a room at that position
				if rooms[col][row]:
					# check to see if theyre in the room
					tmap[col][row] = 'R '
					if rooms[col][row].contains_chest():
						tmap[col][row] = 'C '
					if rooms[col][row].cords == self.active_room.cords:
						tmap[col][row] = 'X '
					if rooms[col][row].contains_exit():
						tmap[col][row] = 'L '
		return self.format_output(tmap)

	def format_output(self,tmap):
		ret = '+-'
		for a in tmap[0]:
		    ret += '--'
		ret += '+\n'
		for a in tmap:
		    ret += '| '
		    for b in a:
		        ret += b
		    ret += '|\n'
		ret += '+'
		for a in tmap[0]:
		    ret += '--'
		ret += '-+\n'
		return ret

class Hub(Dungeon):
	def __init__(self,party):
		""" the hub is the starting area, and it is what the player is always taken back to.
			part: entity.player.players.Party object
		"""
		#self.shop = []
		self.party = party
		self.things=[]
		self.shop = {
			# make sure there is a potion for every single player
			"health":[consumable.HealthPotion() for a in self.party.inventory],
			"weapons":[],
			"armor":[],
			"spells":[], # potions for errybody
			"utility":[]
		}


	def enter_shop(self):
		"""this method is called when the party enters the shop, it handles buying and selling."""
		print 'you have %d gold!' % (self.party.inventory[self.party.index].gold)
		opt = base.make_choice(['Buy','Sell'])
		if opt == 0:
			shopping = base.make_choice(self.shop.keys(),'category')
			item = base.make_choice( ['%s for %d' % (a.to_str(),a.get_cost()) for a in self.shop[self.shop.keys()[shopping]]],'item',True)
			# None can be returned from make_choice when the last parameter is true
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
		elif opt == 1:
			alist = []
			for a in self.party.inventory[self.party.index].inventory:
				try:
					# compile a list of everything that has a price associated with it in the
					# player's inventory
					a.cost
					alist.append(a)
				except:
					pass
			selling = base.make_choice(['%s for %d' % (a.to_str(),a.cost/5) for a in alist],'item',True)
			if selling is not None:
				self.party.inventory[self.party.index].gold+=alist[selling].get_cost()/5
				self.party.inventory[self.party.index].inventory.remove(self.party.inventory[self.party.index].alist[selling])
				self.party.inventory[self.party.index].equipable.remove(self.party.inventory[self.party.index].alist[selling])

		# allow the player to shop as much as they want in a turn
		if base.make_choice(['continue','done']) is 0:
			self.enter_shop()



	def leave_dungeon(self):
		"""called when the player leaves the dungeon"""
		he = [5,8,15,25]
		ind = base.make_choice(['smol','medium','large','goliath'],'size')
		self.party.current_dungeon = Dungeon(he[ind],self.party.get_avg_level(),self.party)
		for a in self.party.inventory:
			a.action_points=a.base_ap
		self.party.current_dungeon.start()
		# base.put(self.party.current_dungeon)

	def save_game(self):
		"""this method is an unused early attempt at making save files work."""
		base.put('Name your save file')
		ans=base.get_input()
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

	def repair_items(self):
		print "Select What you wish to repair."
		select = base.make_choice( ['%s for %d' % (a.to_str(),(a.durability-a.current_durability)*5) for a in self.party.get_active_player().equipable],'item',True)
		#select=base.make_choice(self.party.get_active_player().inventory)
		try:
			amt=self.party.get_active_player().equipable[select].durability-self.party.get_active_player().equipable[select].current_durability
			print "%s costs %d to repair"%(self.party.get_active_player().equipable[select].name,amt*5)
			if base.make_choice(['continue','done']) is 0:
				if self.party.get_active_player().inventory[select].gold>= amt*5:
					self.party.get_active_player().inventory[select].current_durability=self.party.get_active_player().inventory[select].durability
					self.party.get_active_player().inventory[select].gold-=(amt*5)
				else:
					print "You don't have enough gold to do that!"
		except:
			print 'Woops'

	# there are no monsters in the hub
	def handle_monster_turn(self):
		pass

	def start(self):
		"""this method starts the hub and is called after the players enter, it populates the shop."""
		controller = control.ItemController(self.party.get_avg_level())
		for category in self.shop.keys():
			for b in range(random.randint(len(self.party.inventory),len(self.party.inventory)+5)):
				inst = controller.generate(category)
				if inst:
					self.shop[category].append(inst)
		base.put('welcome to the hub!')




class Room(object):
	def __init__(self,containing_dungeon,party):
		""" the class for an individual room in the dungeon
			paramaters:
				containing_dungeon: dungeon.dungeon.Dungeon instance.
				party: entity.player.players.Party instance.
		"""
		self.containing_dungeon = containing_dungeon
		self.neighbors = []
		# the room should only be 50% weaker than the dungeon level or 150% stronger- this is not a mistake
		self.level = math.ceil((random.random() + .5) * containing_dungeon.level)
		self.description = "a %s smelling room, with %s and %s walls and a %s floor." % (random.choice(SMELL),random.choice(TOUCH),random.choice(TOUCH),random.choice(TOUCH))
		# this is to test the generation
		self.test = -9999

		# this will identify the rooms to the players for now
		# this isn't actually used i think
		self.id = random.getrandbits(32)
		self.things = base.Inventory(self)
		# self.identified_things = base.Inventory(self)

		self.party = party

		self.cords = None

		self.directions = {'north':(-1,0),'south':(1,0),'east':(0,1),'west':(0,-1)}
		self.entered = False

	def generate(self):
		""" this method is called recursively on every room, it populates the room with monsters and
			makes other connecting rooms- the dungeon grows like a tree.
			returns:
				rooms_needed: a list of tuples that indicate in which direction new rooms should be generated
		"""
		# use the spawn method in the monster file
		for monstar in monsters.spawn(self.level):
			self.things.append(monstar)
			# set this to the monster's room
			monstar.room=self

		# use the spawn method in the chest file
		chest = chesteses.spawn(self.level)
		if chest:
			self.things.append(chest)

		rooms_needed = []
		# this loop decides whether or not we're spawning a new room in the indicated direction
		for direction, dircords in self.directions.iteritems():
			x,y = dircords
			selfx,selfy = self.cords

			newx = x + selfx
			newy = y + selfy
			ma = self.containing_dungeon.size
			# make sure the cords of a new potential room aren't negative and that there isn't already a room in the space
			if newx >= 0 and newx < ma and newy >=0 and newy < ma and not self.containing_dungeon.rooms[newx][newy]:
				# if there are no neighbors, we want to generate one
				# print len(self.get_neighbors().keys())
				# print len(self.get_neighbors().keys()) <= 1
				if (len(self.get_neighbors().keys()) <= 1):
					rooms_needed.append(self.directions[direction])
					return rooms_needed
				else:
					# if there are less than four, then there is a 10% chance that a new one will happen
					if len(self.get_neighbors().keys()) < 3 and base.D100.roll() <= 5:
						rooms_needed.append(self.directions[direction])
						return rooms_needed
		return rooms_needed

	def get_neighbors(self):
		""" get the room's neighbors
			returns:
				dict of neighbors, structured like {"direction":room_object}
		"""
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

	def get_open_spaces(self):
		ret = []
		ne = self.get_neighbors()
		for direction in self.directions.keys():
			if direction not in ne.keys():
				ret.append(direction)
		return ret

	def is_in_bounds(self,x,y):
		return x >= 0 and y >= 0 and x < self.containing_dungeon.size and y < self.containing_dungeon.size

	def contains_exit(self):
		""" check if the room has an exit
			returns:
				boolean, indicating if the boolean has an exit
		"""
		for a in self.things:
			if isinstance(a,LeaveOption):
				return True
		return False

	def contains_chest(self):
		""" check if the room contains a chest
			returns:
				boolean, indicating if the room has a chest in it
		"""
		for a in self.things:
			if isinstance(a,chesteses.Chest):
				return True
		return False


	def generate_neighbor(self,di):
		"""	generate a neighboring room.
			parameters:
				di: string, either "north" "south" "east" or "west"
		"""
		# base.put('generating n to the %s at %s' % (di,str(self.cords)))
		new_room = Room(self.containing_dungeon,self.party)
		x,y = self.cords

		dirx,diry = self.directions[di]
		new_room.cords = (x+dirx,y+diry)
		self.containing_dungeon.roomslist+=''+str(x+dirx)+' '+str(y+diry)+' '
		self.containing_dungeon.rooms[new_room.cords[0]][new_room.cords[1]] = new_room
		# generation is recursive- call the next room's generate function
		self.containing_dungeon.rooms[new_room.cords[0]][new_room.cords[1]].generate()

	def to_str(self):
		"""deprecated"""
		# this method was a thing at one point, but now it is not. rip
		return self.description

	def move_to(self,ind):
		""" sets the current dungeon's active room to the selected room, and call the enter method on it.
			parameters:
				ind: an int, the index of the room in the keylist of self.neighbors
		"""
		self.containing_dungeon.active_room = self.get_neighbors()[self.get_neighbors().keys()[ind]]
		self.containing_dungeon.active_room.enter()

		##HELP! i need to put all possible neighbors adjacent to a room already in to be ?


	def enter(self):
		""" mark a room as entered"""
		self.entered = True

	def handle_monster_turn(self):
		""" called every turn to let all the monsters do their turn
		"""
		# base.put("THINGS: %s" % str(self.things))
		# base.put('ID: %s' % str(self.identified_things))
		alist=[]
		for thing in self.things:
			if isinstance(thing,monsters.Monster):
				thing.action_points = thing.base_ap
				while thing.alive and thing.action_points > 0:
					thing.do_turn()
					if not thing.alive:
						alist.append(thing)
		for a in alist:
			self.things.remove(a)
		# for thing in self.identified_things:
		# 	if thing.alive:
		# 		thing.do_turn()




class LeaveOption(thing.InteractiveObject):
	def __init__(self):
		""" the object that will allow players to leave the dungeon."""
		super(LeaveOption,self).__init__()
		self.options = ['leave the dungeon']

	def do_turn(self,arg):
		""" overridden from base.Entity, see that documentation """
		if arg == self.options[0]:
			full = False
			for a in self.owner.things:
				if isinstance(a,monsters.Monster):
					full = True
			if full:
				base.put('you can\'t leave the dungeon while you\'re under attack!')
			else:
				for player in self.owner.containing_dungeon.party.inventory:
					player.gold += (self.owner.containing_dungeon.gold_reward / 5)
				base.put('each player is awarded %d gold!' % (self.owner.containing_dungeon.gold_reward / 5))
				self.owner.containing_dungeon.leave_dungeon()

	def to_str(self):
		return 'a ladder out of the dungeon'
