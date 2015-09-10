import random


# Im working here shhh

class Entity(object):
	def __init__(self):
		# not sure about this
		# attack_range = 0
		# self.strength = 0
		# self.perception = 0
		# self.luck = 0
		# self.agility = 0
		# self.mana = 0
		# self.health = 0

		# base ap is what the ap should be restored to after a turn is complete
		self.base_ap = 1
		self.alive = True
		self.action_points = 1
		self.options = []
		self.inventory = []

	def do_turn(self,*options):
		pass

	# def kill(self):
	# 	self.alive = False

	def return_options(self):
		li = []
		li += self.options
		for a in self.inventory: 
			li += a.return_options()
		return li


	def process_options(self,*options):
		pass

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
	
	def roll():
		return random.randint(1,self.num)
D6 = Die(6)
D12 = Die(12)
D20 = Die(20)