import base,random,math
from misc.words import arcane_words, weapon_words
import entity.status.player_statuses as s
import entity.monster.monsters as r



class Item(base.Entity):
	def __init__(self):
		super(Item,self).__init__()
		self.consumes_inventory_space = True
		# THIS PROBABLY IS NOT FINAL
		self.cost = 5
		self.name="item"
		self.equipped = False
		self.descr=self.name+" "+str(self.level)
		self.item_options = []
	def to_str(self):
		return self.name

	def do_turn(self,options):
		pass

	def return_options(self):
		if self.equipped:
			return super(Item,self).return_options()
		return []

	def equip(self):
		if self.info == 'one-handed':
			# this gets the name of the item in both hands, to let the player
			# know what they are going to equip
			if self.owner.equipment['left']:
				left = self.owner.equipment['left'].to_str()
			else:
				left = 'Nothing'

			if self.owner.equipment['right']:
				right = self.owner.equipment['right'].to_str()
			else:
				right = 'Nothing'

			side=base.make_choice(['left (%s)' % left,'right (%s)' % right])
			try:
				if self.owner.equipment[['left','right'][side]].info == 'one-handed':
					self.owner.equipment[['left','right'][side]].unequip()
				else:
					self.owner.equipment['left'].unequip()
					self.owner.equipment['right'].unequip()
			except:
				pass
			try:
				if self.owner.equipment[['left','right'][side]].info == 'one-handed':
					self.owner.equipment[['left','right'][side]]= self
				else:
					self.owner.equipment['left']= None
					self.owner.equipment['right']= None
					self.owner.equipment[['left','right'][side]]= self
			except:
				self.owner.equipment[['left','right'][side]]= self
		elif self.info =='two-handed':
			try:
				self.owner.equipment['left'].unequip()
				self.owner.equipment['right'].unequip()
			except:
				try:
					self.owner.equipment['right'].unequip()
				except:
					pass
			self.owner.equipment['left']=self
			self.owner.equipment['right']=self
		else:
			if not self.owner.equipment[self.info]: name = 'Nothing'
			else: name = self.owner.equipment[self.info].to_str()

			# we want to equip something if we've done it in a test.
			if not base.IS_TEST:
				ans = base.get_input('would you like to replace %s with %s? (y/n) ' % (name,self.to_str()))
			else:
				ans = 'y'
			if ans is 'y':
				if self.owner.equipment[self.info]: self.owner.equipment[self.info].unequip()
				self.owner.equipment[self.info] = self
		self.equipped = True
		# self.name += '*'

	def unequipWep(self):
		self.equipped=False
		if self.owner.equipment['right'] is self:
			self.owner.equipment['right']=None
		if self.owner.equipment['left'] is self:
			self.owner.equipment['left']=Non

	def unequip(self):
		self.equipped = False
		# self.name = self.name[:-1]

	def examine(self):
		try:
			return self.descr
		except:
			return 'a %s' % self.to_str()

	def get_cost(self):
		return self.cost

# this class is for items that we need to be usable at all times, not just while equipped
class ItemUsedFromInventory(Item):
	def __init__(self):
		super(ItemUsedFromInventory,self).__init__()

	def return_options(self):
		return self.options
