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

class Bow(Item):
	def __init__(self,level):
		super(Bow,self).__init__()
		self.name='bow'
		self.level = level
		self.options =['Shoot with %s' % self.to_str, 'Fully Draw the %s' % self.to_str]
		self.damage=7.0 * self.level
	def do_turn(self,option):
		if option == self.options[0]:
			target = self.owner.select_target()
			if target:
				self.shoot(target)

	#an attempt to further increase the action points system. shoot would only cost 1 action point while aim would take 2
	def shoot(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['agility'] + self.owner.attributes['strength'] / 10.0 + base.D12.roll())
	def aim(self,target):
		target.take_damage(self.owner,self.damage + self.owner.attributes['agility']*1.8+ self.owner.attributes['strength']/4.0+base.D20.roll())

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

class Shield(Item):
	def __init__(self,level):
		super(Shield,self).__init__()
		self.name = 'shield'
		self.level = level
		self.options=['Block with %s' %self.to_str,'Defend Allies with' %self.to_str]
		self.armor=10

	#I am not sure how to do the do_turn method.


	#Imagining Blocking will increase armor by a set amount on top of the amount given passively from a shield and cost 1 action point
	#while Defending Allies will increase armor of all Allies (including you) by a set amount and cost 2 action points.

	def block(self,target):
		target.armor+=20

	def defend(self,ally):
		pass


class Breastplate(Item):
	def __init__(self,level):
		super(Breastplate,self).__init__()
		self.name = 'breastplate'
		self.level = level
		self.armor=20

class Chainmail(Item):
	def __init__(self,level):
		super(Chainmail,self).__init__()
		self.name = 'chainmail'
		self.level = level
		self.armor=15

class Platelegs(Item):
	def __init__(self,level):
		super(Platelegs,self).__init__()
		self.name = 'platelegs'
		self.level = level
		self.armor=12

class Helmet(Item):
	def __init__(self,level):
		super(Helmet,self).__init__()
		self.name = 'helmet'
		self.level = level
		self.armor=13