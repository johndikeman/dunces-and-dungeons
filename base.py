import random

D6 = Die(6)
D12 = Die(12)
D20 = Die(20)
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
		self.alive = True

	def do_turn(self):
		pass

	# def kill(self):
	# 	self.alive = False

	def return_options(self):
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