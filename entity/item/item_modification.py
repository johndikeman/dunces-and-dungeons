import base, random, time
import entity.status.player_statuses as s
import math

class ModifyItems(object):
	def __init__(self):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Modified"

class Common(ModifyItems):
	def __init__(self):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Common"

class Basic(Common):
	def __init__(self,item):
		item.pow*=1

	def do_turn(self,target,damage):
		target.take_damage(damage)

	def to_str(self):
		return "Basic"

class Iron(Common):
	def __init__(self,item):
		item.pow*=1.1

	def do_turn(self,target,damage):
		chance=base.D20.roll()
		if chance>19:
			target.statuses.append(s.Maim(1,1))
		target.take_damage(damage)

	def to_str(self):
		return "Iron"

class Rusty(Common):
	def __init__(self,item):
		item.pow*=.5

	def do_turn(self,target,damage):
		chance=base.D20.roll()
		if chance>19:
			target.statuses.append(s.Poison(2,2*self.level))
		target.take_damage(damage)

	def to_str(self):
		return "Rusty"

class Used(Common):
	def __init__(self,item):
		item.pow*=.8

	def do_turn(self,target,damage):
		target.take_damage(damage)

	def to_str(self):
		return "Used"

class Weathered(Common):
	def __init__(self,item):
		item.pow*=.7

	def do_turn(self,target,damage):
		target.take_damage(damage)

	def to_str(self):
		return "Weathered"

class Wooden(Common):
	def __init__(self,item):
		item.pow*=.5

	def do_turn(self,target,damage):
		target.take_damage(damage)

	def to_str(self):
		return "Wooden"

class Notched(Common):
	def __init__(self,item):
		item.pow*=.9

	def do_turn(self,target,damage):
		chance=base.D20.roll()
		if chance>19:
			target.statuses.append(s.Bleeding(2,4*self.level))
		target.take_damage(damage)

	def to_str(self):
		return "Notched"

class Scratched(Common):
	def __init__(self,item):
		item.pow*=.9

	def do_turn(self,target,damage):
		target.take_damage(damage)

	def to_str(self):
		return "Scratched"

class Uncommon(ModifyItems):
	def __init__(self,item):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Uncommon"

class Good(Uncommon):
	def __init__(self,item):
		item.pow*=1.3

	def do_turn(self,target,damage):
		target.take_damage(damage)

	def to_str(self):
		return "Good"

class Shining(Uncommon):
	def __init__(self,item):
		item.pow*=1.6

	def do_turn(self,target,damage):
		target.take_damage(damage)

	def to_str(self):
		return "Shining"

class Steel(Uncommon):
	def __init__(self,item):
		item.pow*=1.3

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			target.statuses.append(s.Bleeding(3,3*self.level))
		chance2 = base.D20.roll()
		if chance2 > 18:
			target.statuses.append(s.Maim(2,2))
		target.take_damage(damage)

	def to_str(self):
		return "Steel"

class Archaic(Uncommon):
	def __init__(self,item):
		item.pow*=1.3

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			target.statuses.append(s.Poison(3,3*self.level))
		target.take_damage(damage)

	def to_str(self):
		return "Archaic"

class Brutal(Uncommon):
	def __init__(self,item):
		item.pow*=1.5

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			target.statuses.append(s.Bleeding(3,3*self.level))
		chance2 = base.D20.roll()
		if chance2 > 16:
			target.statuses.append(s.Maim(1,3))
		target.take_damage(damage)

	def to_str(self):
		return "Brutal"

class Rare(ModifyItems):
	def __init__(self,item):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Rare"

class Ceremonial(Rare):
	def __init__(self,item):
		item.pow*=2.5

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			self.owner.owner.gold+=self.level
		target.take_damage(damage)

	def to_str(self):
		return "Ceremonial"

class Silver(Rare):
	def __init__(self,item):
		item.pow*=2.4

	def do_turn(self,target,damage):
		#not finished, make wolves weak to it.
		target.take_damage(damage)

	def to_str(self):
		return "Silver"

class Killing(Rare):
	def __init__(self,item):
		item.pow*=3

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			damage*=((chance-16)/2)+base.D20.roll()
		target.take_damage(damage)

	def to_str(self):
		return "Killing"

class Blessed(Rare):
	def __init__(self,item):
		item.pow*=3.2

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 18:
			target.statuses.append(s.Blind(math.round(math.pow(1.1,self.level))))
		target.take_damage(damage)

	def to_str(self):
		return "Blessed"

class Legendary(ModifyItems):
	def __init__(self,item):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Legendary"

class Kingly(Legendary):
	def __init__(self,item):
		item.pow*=4

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			self.owner.owner.gold+=self.level*1.5
		target.take_damage(damage)

	def to_str(self):
		return "Kingly"

class Enchanted(Legendary):
	def __init__(self,item):
		item.pow*=4.2

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 18:
			target.statuses.append(s.Sleep())
		target.take_damage(damage)

	def to_str(self):
		return "Enchanted"

class Master(Legendary):
	def __init__(self,item):
		item.pow*=4.6

	def do_turn(self,target,damage):
		chance = base.D20.roll()
		if chance > 16:
			damage *= 2.5
		chance2 = base.D20.roll()
		if chance2 > 16:
			target.statuses.append(s.Maim(2))
		chance3 = base.D20.roll()
		if chance3 > 16:
			target.statuses.append(s.Bleeding(2,self.level*6))
		target.take_damage(damage)

	def to_str(self):
		return "Master"

class Divined(ModifyItems):
	def __init__(self,item):
		pass

	def do_turn(self,target,damage):
		pass

	def to_str(self):
		return "Divine"

class Celestial(Divined):
	def __init__(self,item):
		item.pow*=6

	def do_turn(self,target,damage):
		chance=base.D40.roll()
		if chance>39:
			print "A blinding light flashes from the Heavens and blinds and reveals all enemies in the room!"
			print 'Hey if there is an error its on 323 of item_modification.py'
			for a in self.owner.owner.party.current_dungeon.active_room.things:
				a.statuses.append(s.Blind(6))
		target.take_damage(damage)

	def to_str(self):
		return "Celestial"

class Divine(Divined):
	def __init__(self,item):
		item.pow*=6.8

	def do_turn(self,target,damage):
		chance = base.D40.roll()
		if chance > 39:
			print 'Power surges through your body giving you increased damage and speed!'
			self.owner.owner.action_points+=3
			damage*=4
		target.take_damage(damage)

	def to_str(self):
		return "Divine"

class Heavenly(Divined):
	def __init__(self,item):
		item.pow*=6.4

	def do_turn(self,target,damage):
		chance = base.D40.roll()
		if chance > 39:
			print 'Heavenly Fire leaps from the body of your enemy, striking all enemies in the room'
			print 'Hey if there is an error its on 354 of item_modification.py'
			for a in self.owner.owner.party.current_dungeon.active_room.things:
				a.take_damage(20*self.level)
				chance2=base.D20.roll()
				if chance2>14:
					a.statuses.append(s.Burn(self.level,self.level*8))
		target.take_damage(damage)

	def to_str(self):
		return "Heavenly"

class Arch(Divined):
	def __init__(self,item):
		item.pow*=8

	def do_turn(self,target,damage):
		chance=base.D100.roll()
		if chance >99:
			print 'The Arch Powers of the World infuse your body!'
			print 'Mortal Strike!'
			target.statuses.append(s.Burn(self.level,100))
			target.statuses.append(s.Poison(self.level,120))
			target.statuses.append(s.Bleeding(self.level,1000))
			target.statuses.append(s.Maim(self.level))
			target.statuses.append(s.Stun(self.level/2))
			target.statuses.append(s.Sleep())
			target.statuses.append(s.Blind(self.level*2))
			for a in self.owner.owner.party.inventory:
				a.statuses.append(s.Healing())
			damage*=10
		target.take_damage(damage)

	def to_str(self):
		return "Arch"
