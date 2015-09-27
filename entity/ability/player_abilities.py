import base,math,random
import entity.status.player_statuses as s
from misc.words import arcane_words

class BattleCry(base.Entity):
	def __init__(self):
		super(BattleCry,self).__init__()
		self.options = ['cast BattleCry']
		self.level = 1

	# roll a d10. if the roll is over 5, then you attract all the aggro of all the monsters
	def do_turn(self,option):
		if option == self.options[0]:
			roll = base.D10.roll()
			if roll > 5:
				# if the roll is 10, you do damage to all monsters based on half your strength.
				if roll == 10:
					print 'BattleCry critical success!'
					for a in self.owner.current_dungeon.current_room.things:
						a.aggro = self.owner
						a.take_damage(self.owner,self.owner.attributes['strength'] * .5)
				else:	
					print 'BattleCry successfully cast!'
					for a in self.owner.current_dungeon.current_room.things:
							a.aggro = self.owner
			# if the roll is one, you do the damage to all your party.
			elif roll == 1:
				print 'BattleCry critical fail!'
				for party_member in self.owner.party.inventory:
					party_member.take_damage(self.owner,self.owner.attributes['strength'] * .5)


class ShieldBash(base.Entity):
	def __init__(self):
		super(BattleCry,self).__init__()
		self.options = ['cast ShieldBash']
		self.level = 1

	def do_turn(self,option):
		target = self.owner.select_target()
		if target:
			# TODO- implement stun
			target.statuses.append(s.Stun(2))


class SpellBook(base.Entity):
	def __init__(self,level):
		self.level = level
		self.name = ''
		for a in range(int(math.ceil(level))):
			self.name += " %s" % random.choice(arcane_words)
		self.options = ['cast %s' % self.name,'rename %s' % self.name]
		self.stuntime = random.choice(range(level * 4))
		self.poisontime = random.choice(range(level * 4))
		self.damage = random.choice(range(-20*level,20*level))
		self.poisondamage = random.choice(range(-5*level,5*level))
		self.aoe = random.choice([True,False])

	def do_turn(self,option):
		# effectiveness coefficient
		ec = self.owner.attributes['mana'] / 5
		if option == self.options[1]:
			name = raw_input('enter a new name for %s' % self.name)
			self.name = name
		if option == self.options[0]:
			if not self.aoe:
				targets = [self.owner.select_target()]
			else:
				targets = self.owner.party.current_dungeon.active_room.things
			for target in targets:
				if target:
					if damage:
						target.take_damage(damage*ec)
					if stuntime:
						target.statuses.append(s.Stun(math.ceil(stuntime*ec)))
					if poisontime and poisondamage:
						target.statuses.append(s.Poison(math.ceil(poisontime*ec),poisondamage*ec))

	def to_str(self):
		ret =  "%s does %.2f damage, stuns for %d turns and does %.2f of poison damage every turn for %d turns " % (self.name,self.damage,self.stuntime,self.poisondamage,self.poisontime)
		if self.aoe:
			ret += 'in an area of effect.'
		else:
			ret += 'to a single target.'
		return ret

class ArcaneGenerator(base.Entity):
	def __init__(self):
		self.chromosomes = []



