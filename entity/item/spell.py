import entity.item.items as item
import random, math, base
from misc.words import arcane_words
import entity.status.player_statuses as s

class SpellBook(item.Item):
	def __init__(self,level):
		super(SpellBook,self).__init__()
		self.info = 'one-handed'
		self.info2='nope'
		self.cost = random.randint(0,10)
		# base.put(type(level))

		self.level = level
		self.name = ''
		# hahahahahaha this is so stupid
		for a in range(int(self.level)):
			self.name += "%s " % random.choice(arcane_words)
		self.options = ['%s' % self.name]
		# the stuntime maxes out around 5 turns
		self.stuntime = random.random() * math.log(2,level+1)
		self.poisontime = random.random() * (level * 4)
		self.damage = (random.random() * (20*level))
		self.poisondamage = (random.random() * (10*level))
		self.aoe = random.choice([True,False])
		self.on_cooldown = False
		self.cooldown_time = random.random() * math.log(2,level+1) + 1
		self.item_options = ['equip','examine']

		self.is_healing = False

	def do_turn(self,option):
		# effectiveness coefficient
		ec = self.owner.attributes['mana'] / 5
		if option == self.options[0]:
			p = base.make_choice(['cast %s' % self.name,'rename %s' % self.name,'examine %s' % self.name])
			if p == 1:
				name = base.get_input('enter a new name for %s' % self.name)
				self.name = name
				self.options = ['%s' % self.name]

			if p == 2:
				base.put(self.ploop())

			if p == 0:
				if not self.on_cooldown:
					if not self.is_healing:
						if not self.aoe:
							self.murder(self.owner.select_target())
							self.owner.statuses.append(s.Cooldown(self,self.cooldown_time))
						else:
							self.owner.do_aoe_monster(self.murder)
							self.owner.statuses.append(s.Cooldown(self,self.cooldown_time))
					else:
						if not self.aoe:
							self.murder(self.owner.select_player_target())
							self.owner.statuses.append(s.Cooldown(self,self.cooldown_time))
						else:
							self.owner.do_aoe_player(self.murder)
							self.owner.statuses.append(s.Cooldown(self,self.cooldown_time))

				else:
					base.put('%s is on cooldown!' % self.name)

	def murder(self,target):
		ec = self.owner.attributes['mana'] / 5
		if target:
			if self.damage:
				target.take_damage(self.owner,self.damage*ec)
			if self.stuntime:
				target.statuses.append(s.Stun(math.ceil(self.stuntime)))
			if self.poisontime and self.poisondamage:
				target.statuses.append(s.Poison(math.ceil(self.poisontime),self.poisondamage*ec))

	def to_str(self):
		return 'a spell by the name of %s' % self.name

	def ploop(self):
		ret =  "%s does %.2f damage, stuns for %d turns and does %.2f of poison damage every turn for %d turns, with a cooldown of %d turns" % (self.name,self.damage,self.stuntime,self.poisondamage,self.poisontime,self.cooldown_time)
		if self.aoe:
			ret += 'in an area of effect.'
		else:
			ret += 'to a single target.'
		return ret

	def examine(self):
		return self.ploop()

	def get_cost(self):
		return 20 * (10/self.cooldown_time)
