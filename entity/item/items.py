import base

class Item(base.Entity):
	def __init__(self):
		super(Item,self).__init__()
		self.consumes_inventory_space = True

	def to_str(self):
		return self.name

	def do_turn(self,options):
		pass

class Sword(Item):
	def __init__(self,level):
		super(Sword,self).__init__()
		self.name = 'sword'
		self.level = level
		self.options = ['attack with %s' % self.to_str()]
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

class Dagger(Item):
	def __init__(self,level):
		self.name = 'dagger'
		self.level = level
		super(Sword,self).__init__()
		self.options = ['attack with %s' % self.to_str()]
		self.damage = 5.0 * self.level
		

	def do_turn(self,option):
		if option == self.options[0]:
			target = self.owner.select_target()
			if target:
				self.swing(target)

	def swing(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['strength'] / 2.0 + self.owner.attributes['agility'] / 2.0 + base.D20.roll())


class Flail(Item):
	def __init__(self,level):
		self.name = 'flail'
		self.level = level
		super(Sword,self).__init__()
		self.options = ['attack with %s' % self.to_str()]
		self.damage = 4.0 * self.level

	def do_turn(self,option):
		if option == self.options[0]:
			target = self.owner.select_target()
			if target:
				self.swing(target)

	def swing(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['strength'] / 2.0 + self.owner.attributes['agility'] + self.owner.attributes['luck'] + base.D20.roll())






