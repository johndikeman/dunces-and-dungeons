import entity.item.items
import base,random,math
import entity.monster.monsters as r


class Weapon(entity.item.items.Item):
	def __init__(self):
		super(Weapon,self).__init__()

	def get_cost(self):
		return self.cost

class Sword(Weapon):
	def __init__(self,level):
		super(Sword,self).__init__()
		self.name = 'sword'
		self.info='one-handed'
		self.info2='weapon'
		self.level = level
		self.descr=self.name+" "+str(self.level)
		self.options = ['%s' % self.to_str()]
		self.item_options=['examine','equip']
		self.damage = 7.0 * self.level
		self.cost = 10

	def do_turn(self,options):
		self.damage = 7.0 * self.owner.level
		self.options = ['%s' % self.to_str()]
		# print options
		if self.options[0] in options:
			p = base.make_choice(['swing %s' % self.to_str()])
			if p == 0:
				target = self.owner.select_target()
				if target:
					for a in self.modifiers:
						a.do_turn(target,self.standard_attack(target))
					

	def standard_attack(self,target):
		return self.damage + self.owner.attributes['strength'] + base.D12.roll()

class Dagger(Weapon):
	def __init__(self,level):
		super(Dagger,self).__init__()
		self.name = 'dagger'
		self.level = level
		self.descr=self.name+" "+str(self.level)
		self.info='one-handed'
		self.info2='weapon'
		self.item_options=['examine','equip']
		self.options = ['%s' % self.to_str()]
		self.cost= 7.0
		self.damage = 5.0 * self.level


	def do_turn(self,option):
		self.damage = 5.0 * self.owner.level
		self.options = ['%s' % self.to_str()]

		if option == self.options[0]:
			p = base.make_choice(['attack with %s' % self.to_str()])
			if p == 0:
				target = self.owner.select_target()
				if target:
					for a in self.modifiers:
						a.do_turn(target,self.standard_attack(target))

	def standard_attack(self,target):
		return self.damage + self.owner.attributes['strength'] / 2.0 + self.owner.attributes['agility'] / 2.0 + base.D20.roll()

class Bow(Weapon):
	def __init__(self,level):
		super(Bow,self).__init__()
		self.name='bow'
		self.info='two-handed'
		self.info2='weapon'
		self.level = level
		self.descr=self.name+" "+str(self.level)
		self.cost=10.0
		self.item_options=['examine','equip']
		self.options = ['%s' % self.to_str()]
		self.damage=1.0 * (25 * math.log(self.level + 1, 2) + 3) / 50.0

	def add_to_inventory(self):
		# we want rangers to be super effective with bows
		if self.owner.race is 'Ranger':
			self.damage *= 2

	def do_turn(self,option):
		if self.owner.race is 'Ranger':
			self.damage = 7.0 * self.owner.level*2.0
		else:
			self.damage = 1.0 * self.owner.level
		self.options = ['%s' % self.to_str()]
		if option == self.options[0]:
			p = base.make_choice(['Shoot with %s' % self.to_str(), 'Fully draw the %s' % self.to_str(), 'Launch Volley'])
			if p == 0:
				target = self.owner.select_target()
				if target:
					for a in self.modifiers:
						a.do_turn(target,self.damage * (self.owner.attributes['agility'] + self.owner.attributes['strength'] / 10.0) + base.D12.roll())
			elif p == 1:
				target = self.owner.select_target()
				if target:
					self.aim(target)
			elif p == 2:
				# THIS IS THE NEW AOE CODE.
				self.owner.do_aoe_monster(self.volley)


	#an attempt to further increase the action points system. shoot would only cost 1 action point while aim would take 2
	def standard_attack(self,target):
		return self.damage * (self.owner.attributes['agility'] + self.owner.attributes['strength'] / 10.0)
		
	def aim(self,target):
		for a in self.modifiers:
			a.do_turn(target,self.damage * (self.owner.attributes['agility'] * 1.9 + self.owner.attributes['strength']/4.0) + base.D20.roll())
		self.owner.action_points -= 1
	def volley(self,target):
		for a in self.modifiers:
			a.do_turn(target,self.damage*.1 + self.owner.attributes['agility']*.1+self.owner.attributes['strength']*.1 + self.owner.attributes['intelligence']*.1+self.owner.attributes['luck']*.1)


class Rapier(Weapon):
	def __init__(self,level):
		super(Rapier,self).__init__()
		self.level=level
		self.name='rapier'
		self.info='one-handed'
		self.info2='weapon'
		self.descr=self.name+" "+str(self.level)
		self.item_options=['examine','equip']
		self.options = ['%s' % self.to_str()]
		self.cost=8.0
		self.damage = 2.0 * self.level

	def do_turn(self,option):
		self.damage = 2.0 * self.owner.level
		self.options = ['%s' % self.to_str()]
		if option == self.options[0]:
			p = base.make_choice(['Slash with %s' % self.to_str(),'Pierce Armor with %s'%self.to_str()])
			if p == 0:
				target = self.owner.select_target()
				if target:
					for a in self.modifiers:
						a.do_turn(target,self.standard_attack(target))
			elif p == 1:
				target = self.owner.select_target()
				if target:
					self.pierce(target)

	def standard_attack(self,target):
		return self.damage+self.owner.attributes['agility']
	def pierce(self,target):
		hold=target.armor
		target.armor = 0
		for a in self.modifiers:
			a.do_turn(target,self.damage + self.owner.attributes['strength'] / 5.0 + self.owner.attributes['agility']/2.0 + self.owner.attributes['intelligence']/4.0 +hold+ base.D20.roll())
		target.armor=hold

class Flail(Weapon):
	def __init__(self,level):
		super(Flail,self).__init__()
		self.level = level

		self.name = 'flail'
		self.info='one-handed'
		self.info2='weapon'
		self.cost=8.0
		self.descr=self.name+" "+str(self.level)
		self.item_options=['examine','equip']
		self.options = ['%s' % self.to_str()]
		self.damage = 4.0 * self.level

	def do_turn(self,option):
		self.damage = 4.0 * self.owner.level
		self.options = ['%s' % self.to_str()]
		if option == self.options[0]:
			p = base.make_choice(['attack with %s' % self.to_str()])
			if p == 0:
				target = self.owner.select_target()
				if target:
					for a in self.modifiers:
						a.do_turn(target,self.standard_attack(target))
						

	def standard_attack(self,target):
		return self.damage + self.owner.attributes['strength'] / 2.0 + self.owner.attributes['agility'] + self.owner.attributes['luck'] + base.D20.roll()
		
