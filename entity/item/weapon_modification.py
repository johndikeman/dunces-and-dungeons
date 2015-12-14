import base, random, time
import entity.status.player_statuses as s
import math

class ModifyItems(base.Entity):
	def __init__(self):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Modified"

class Common(ModifyItems):
	def apply(self):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Common"

class Basic(Common):
	def apply(self):
		self.owner.cost=self.owner.cost*10
		self.owner.damage*=1

	def do_turn(self,target,damage):
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Basic"

class Iron(Common):
	def apply(self):
		self.owner.cost=self.owner.cost*11
		self.owner.damage*=1.1

	def do_turn(self,target,damage):
		chance=base.D20.roll()
		if chance>19:
			target.statuses.append(s.Maim(1,1))
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Iron"

class Rusty(Common):
	def apply(self):
		self.owner.cost=self.owner.cost*7
		self.owner.damage*=.5

	def do_turn(self,target,damage):
		chance=base.D20.roll()
		if chance>19:
			target.statuses.append(s.Poison(2,2*self.owner.level))
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Rusty"

class Used(Common):
	def apply(self):
		self.owner.cost=self.owner.cost*7.5
		self.owner.damage*=.8

	def do_turn(self,target,damage):
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Used"

class Weathered(Common):
	def apply(self):
		self.owner.cost=self.owner.cost*7
		self.owner.damage*=.7

	def do_turn(self,target,damage):
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Weathered"

class Wooden(Common):
	def apply(self):
		self.owner.cost=self.owner.cost*5
		self.owner.damage*=.5

	def do_turn(self,target,damage):
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Wooden"

class Notched(Common):
	def apply(self):
		self.owner.cost=self.owner.cost*8.5
		self.owner.damage*=.9

	def do_turn(self,target,damage):
		chance=base.D20.roll()
		if chance>19:
			target.statuses.append(s.Bleeding(2,4*self.owner.level))
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Notched"

class Scratched(Common):
	def apply(self):
		self.owner.cost=self.owner.cost*9
		self.owner.damage*=.9

	def do_turn(self,target,damage):
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Scratched"

class Uncommon(ModifyItems):
	def apply(self):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Uncommon"

class Good(Uncommon):
	def apply(self):
		self.owner.cost=self.owner.cost*15
		self.owner.damage*=1.3

	def do_turn(self,target,damage):
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Good"

class Shining(Uncommon):
	def apply(self):
		self.owner.cost=self.owner.cost*20
		self.owner.damage*=1.6

	def do_turn(self,target,damage):
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Shining"

class Steel(Uncommon):
	def apply(self):
		self.owner.cost=self.owner.cost*16
		self.owner.damage*=1.3

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			target.statuses.append(s.Bleeding(3,3*self.owner.level))
		chance2 = base.D20.roll()
		if chance2 > 18:
			target.statuses.append(s.Maim(2,2))
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Steel"

class Archaic(Uncommon):
	def apply(self):
		self.owner.cost=self.owner.cost*16
		self.owner.damage*=1.3

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			target.statuses.append(s.Poison(3,3*self.owner.level))
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Archaic"

class Brutal(Uncommon):
	def apply(self):
		self.owner.cost=self.owner.cost*20
		self.owner.damage*=1.5

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			target.statuses.append(s.Bleeding(3,3*self.owner.level))
		chance2 = base.D20.roll()
		if chance2 > 16:
			target.statuses.append(s.Maim(1,3))
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Brutal"

class Rare(ModifyItems):
	def apply(self):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Rare"

class Ceremonial(Rare):
	def apply(self):
		self.owner.cost=self.owner.cost*40
		self.owner.damage*=2.5

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			self.owner.owner.gold+=self.owner.level
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Ceremonial"

class Silver(Rare):
	def apply(self):
		self.owner.cost=self.owner.cost*38
		self.owner.damage*=2.4

	def do_turn(self,target,damage):
		#not finished, make wolves weak to it.
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Silver"

class Killing(Rare):
	def apply(self):
		self.owner.cost=self.owner.cost*50
		self.owner.damage*=3

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			damage*=((chance-16)/2)+base.D20.roll()
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Killing"

class Blessed(Rare):
	def apply(self):
		self.owner.cost=self.owner.cost*55
		self.owner.damage*=3.2

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 18:
			target.statuses.append(s.Blind(round(math.pow(1.1,self.owner.level))))
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Blessed"

class Legendary(ModifyItems):
	def apply(self):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Legendary"

class Kingly(Legendary):
	def apply(self):
		self.owner.cost=self.owner.cost*75
		self.owner.damage*=4

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			self.owner.owner.gold+=self.owner.level*1.5
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Kingly"

class Enchanted(Legendary):
	def apply(self):
		self.owner.cost=self.owner.cost*80
		self.owner.damage*=4.2

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 18:
			target.statuses.append(s.Sleep())
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Enchanted"

class Master(Legendary):
	def apply(self):
		self.owner.cost=self.owner.cost*100
		self.owner.damage*=4.6

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			damage *= 2.5
		chance2 = base.D20.roll()
		if chance2 > 16:
			target.statuses.append(s.Maim(4,2))
		chance3 = base.D20.roll()
		if chance3 > 16:
			target.statuses.append(s.Bleeding(2,self.owner.level*6))
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Master"

class Divined(ModifyItems):
	def apply(self):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Divine"

class Celestial(Divined):
	def apply(self):
		self.owner.cost=self.owner.cost*150
		self.owner.damage*=6

	def do_turn(self,target,damage):
		chance=base.D40.roll()
		if chance>39:
			print "A blinding light flashes from the Heavens and blinds and reveals all enemies in the room!"
			print 'Hey if there is an error its on 323 of self.owner_modification.py'
			for a in self.owner.owner.party.current_dungeon.active_room.things:
				if isinstance(a,Monster):
					a.statuses.append(s.Blind(6))
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Celestial"

class Divine(Divined):
	def apply(self):
		self.owner.cost=self.owner.cost*200
		self.owner.damage*=6.8

	def do_turn(self,target,damage):
		chance = base.D40.roll()
		if chance > 39:
			print 'Power surges through your body giving you increased damage and speed!'
			self.owner.owner.action_points+=3
			damage*=4
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Divine"

class Heavenly(Divined):
	def apply(self):
		self.owner.cost=self.owner.cost*250
		self.owner.damage*=6.4

	def do_turn(self,target,damage):
		chance = base.D40.roll()
		if chance > 39:
			print 'Heavenly Fire leaps from the body of your enemy, striking all enemies in the room'
			print 'Hey if there is an error its on 354 of self.owner_modification.py'
			for a in self.owner.owner.party.current_dungeon.active_room.things:
				if isinstance(a,Monster):
					a.take_damage(self.owner,20*self.owner.level)
					chance2=base.D20.roll()
					if chance2>14:
						a.statuses.append(s.Burn(self.owner.level,self.owner.level*8))
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Heavenly"

class Arch(Divined):
	def apply(self):
		self.owner.cost=self.owner.cost*500
		self.owner.damage*=8

	def do_turn(self,target,damage):
		chance=base.D100.roll()
		if chance >99:
			print 'The Arch Powers of the World infuse your body!'
			print 'Mortal Strike!'
			target.statuses.append(s.Burn(self.owner.level,100))
			target.statuses.append(s.Poison(self.owner.level,120))
			target.statuses.append(s.Bleeding(self.owner.level,1000))
			target.statuses.append(s.Maim(self.owner.level))
			target.statuses.append(s.Stun(self.owner.level/2))
			target.statuses.append(s.Sleep())
			target.statuses.append(s.Blind(self.owner.level*2))
			for a in self.owner.owner.party.inventory:
				a.statuses.append(s.Healing())
			damage*=10
		target.take_damage(self.owner.owner,damage)

	def to_str(self):
		return "Arch"
