import base

class Item(base.Entity):
	def __init__(self):
		super(Item,self).__init__()
		self.consumes_inventory_space = True

	def to_str(self):
		return "this is the item superclass. if you're reading this you really shouldn't be"

	def do_turn(self,options):
		pass

class Sword(Item):
	def __init__(self):
		super(Sword,self).__init__()
		self.options = ['swing %s' % self.to_str()]
		self.damage = 10.0 * self.level
		
	def do_turn(self,options):
		# print options
		if self.options[0] in options:
			# print 'swing mah sword'
			target =  self.owner.select_target()
			if target:
				self.swing(target)

	def swing(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['strength'] + base.D12.roll())

	def to_str(self):
		return 'sword'



