
import base
import entity.item.items as items

# inventory is the exact same thing as list, except it 
# installs a backref to itself (and therefore the player/entity)
# to everything that is added to it
class PlayerInventory(base.Inventory):
	def __init__(self,owner):
		super(PlayerInventory,self).__init__(owner)
		self.space = 6

	def append(self,thing):
		if isinstance(thing,items.Item) and thing.consumes_inventory_space:
			if self.space > 0:
				self.space -= 1
				super(Inventory,self).append(thing)
			else:
				print 'No more inventory space!'

