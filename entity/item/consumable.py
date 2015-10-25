import entity.item.items.Item


# this extends item but overrides return_options to allow it to return an option
# if it isnt equipped
class Consumable(entity.item.items.Item):
	def __init__(self):
		super(Consumable,self).__init__()

	def return_options(self):
		return self.options

class HealthPotion(Consumable):
	def __init__(self):
		super(HealthPotion,self).__init__()
		self.options = ['drink health potion']
		self.name = 'health potion'
		self.cost = 20
	def do_turn(self,option):
		# the player can only have one health potion active at a time
		if option == self.options[0] and not self.owner.statuses.contains_type(s.Healing):
			print "%s consumes a health potion!" % self.owner.name
			self.owner.statuses.append(s.Healing())
			self.owner.inventory.remove(self)

class Sack(Consumable):
	def __init__(self,contents):
		super(Sack,self).__init__()
		self.contents = contents
		self.options = ['open sack']
		self.name = 'a rugged sack'

	def do_turn(self,option):
		if option == 'open sack':
			de = ''
			for a in self.contents:
				self.owner.inventory.append(a)
				de += '%s, ' % a.name
			print 'you open the sack and find %s' % de[:-2]
			self.owner.inventory.remove(self)