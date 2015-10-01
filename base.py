import random, math, time

class Entity(object):
	def __init__(self):
		# ATTRIBUTES
		self.attributes = {'strength':0,'intelligence':0,'luck':0,'agility':0,'mana':0}

		self.health = 0.0
		self.level = 1
		# base ap is what the ap should be restored to after a turn is complete
		self.base_ap = 1
		self.alive = False
		self.action_points = 1
		self.options = []
		self.inventory = Inventory(self)
		self.statuses = Inventory(self)
		self.owner = None
		self.armor = 1
		self.id = random.random() * 100000000
	def do_turn(self,options):
		pass


	def examine(self):
		pass
	# def kill(self):
	# 	self.alive = False

	def return_options(self,inv=True):
		li = []
		li += self.options
		if inv:
			for a in self.inventory: 
				li += a.return_options()
			return li
		return li


	def mod_armor(self,val):
		self.armor += val
		if self.armor < 1:
			self.armor = 1

	# these methods are going to be used for armor and shit to apply their augments
	def apply(self):
		pass

	def exit(self):
		pass


	def take_damage(self,attacker,damage):
		damage = float(damage)
		# compute damage resistance based on the armor
		res = (25 * math.log(self.armor + 1, 11) + 3) / 100.0
		damage -= (damage * res)
		if(damage<0):
			damage=0
		print '(%s) takes (%.2f) damage from (%s)' % (self.to_str(),damage,attacker.to_str())
		self.health -= damage
		if self.health <= 0:
			self.alive = False
			print "(%s) has died by the hand of (%s)" % (self.to_str(),attacker.to_str())
		time.sleep(1)


	# def process_options(self,*options):
	# 	pass

# this is a superclass for general traps
class Trap(object):
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


class Die(object):
	def __init__(self,num):
		self.num = num
	
	def roll(self):
		return random.randint(1,self.num)


# inventory is the exact same thing as list, except it 
# installs a backref to itself (and therefore the player/entity)
# to everything that is added to it
class Inventory(list):
	def __init__(self,owner):
		super(Inventory,self).__init__()
		self.owner = owner
		self.space = 6

	def append(self,thing):
		thing.owner = self.owner
		thing.apply()

		super(Inventory,self).append(thing)

	def remove(self,object_to_remove):
		object_to_remove.exit()
		# print 'base remove method called!'
		for ind, obj in enumerate(self):
			if obj.id == object_to_remove.id:
				self = self[:ind] + self[ind+1:]




# use this method when you have a list of things that the 
# player needs to choose from. it will be handy later on 
# i think
def make_choice(choices,thing=None):
	if len(choices) <= 0:
		print 'nothing to choose from!'
		return
	if thing:
		print 'choose a %s' % thing
	else:
		print 'choose one!'
	for ind, a in enumerate(choices):
		print "\t%s (%d)\n" % (a, ind)

	ans = raw_input()
	try:
		ret = int(ans)
		if ret > len(choices)-1:
			print 'that wasn\'t a choice! try again.'
			return make_choice(choices,thing)
	except ValueError:
		print 'that wasn\'t a choice! try again.'
		return make_choice(choices,thing)
	return ret

def shop_make_choice(choices,choiceskeys,thing=None):
	choices.append("Back")
	choiceskeys.append(0)
	if len(choices) <= 0:
		print 'nothing to choose from!'
		return
	if thing:
		print 'choose a %s' % thing
	else:
		print 'choose one!'
	for ind, a in enumerate(choices):
		print "\t%s for %d (%d)\n" % (a, choiceskeys[ind], ind)

	ans = raw_input()
	try:
		ret = int(ans)
		if ret > len(choices)-1:
			print 'that wasn\'t a choice! try again.'
			return make_choice(choices,thing)
	except ValueError:
		print 'that wasn\'t a choice! try again.'
		return make_choice(choices,thing)
	return choices[ret]

D2 = Die(2)
D6 = Die(6)
D12 = Die(12)
D20 = Die(20)