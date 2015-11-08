import base, random
import entity.monster.monsters as m
import entity.status.monster_statuses as status
import entity.status.player_statuses as p_status
import entity.monster.monster_modification as mods


class ChemicalOgre(m.Monster):
    def __init__(self,level):
        super(ChemicalOgre,self).__init__(level)
        self.health = self.level * 700
        self.max_health = self.level * 700
        self.power = self.level * 200
        self.action_points = 4
        self.base_ap = 4
        self.animals = 'horse cow sheep giraffe anteater anchovie dolphin dog cat antelope hippo whale'.split(' ')

    def do_turn(self):
        for a in self.statuses:
            a.do_turn(None)
        self.check_if_alive()

        if self.action_points > 0:
            roll = base.D6.roll()
            if roll is 1:
                self.smash()
            if roll is 2:
                self.enrage()
            if roll is 3:
                self.autoattack()
            if roll is 4:
                self.feast()
            if roll is 5 or roll is 6:
                print "the ogre looks around, apparently confused."

        self.action_points -= 1

    def smash(self):
        self.reveal()
        print 'the ogre roars and smashes the floor!'
        for player in self.owner.party.inventory:
            player.take_damage(self,self.power/3)

    def enrage(self):
        self.reveal()
        print 'the ogre is enraged, and has gotten stronger!'
        self.statuses.append(status.OgreEnrage())

    def autoattack(self):
        self.reveal()
        if self.action_points > 0:
			if not self.aggroed:
				self.select_aggro()

			if self.aggro.alive:
				self.attack(self.aggro)

    def feast(self):
        self.reveal()
        print 'the ogre eats an entire %s!! where did it even get that??' % random.choice(self.animals)
        self.health += (self.max_health * .05)

    def poison_splash(self):
        self.reveal()
        print 'the ogre pours a cask of poisonous sludge all over your party!'
        for player in self.owner.party.inventory:
            player.statuses.append(p_status.Poison(3,self.power * .1))

    def to_str(self):
        return "She'rak the Chemical Ogre"

class SpiderQueen(m.Monster):
    def __init__(self,level):
        super(SpiderQueen,self).__init__(level)
        self.health = self.level * 400
        self.power = self.level * 100

    def do_turn(self):
        for a in self.statuses:
            a.do_turn(None)
        self.check_if_alive()

        if self.action_points > 0:
            roll = base.D6.roll()
            if roll >= 3:
                self.spawn_spiderlings()
            else:
                self.autoattack()

        self.action_points -= 1

    def spawn_spiderlings(self):
        self.reveal()
        num = base.D20.roll()
        print "the spider queen births %d new spiderlings!" % num
        for a in range(num):
            self.owner.things.append(m.Spiderling(self.level))

    def autoattack(self):
        self.reveal()
        if self.action_points > 0:
            if not self.aggroed:
                self.select_aggro()

        if self.aggro.alive:
            self.attack(self.aggro)
            self.aggro.statuses.append(p_status.Poison(5,self.power/4))

    def to_str(self):
        return "Araknai the Spider Queen"

boss_options = [ChemicalOgre, SpiderQueen]
