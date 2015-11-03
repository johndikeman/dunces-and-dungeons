import base
import entity.monster.monsters as m
import entity.status.monster_statuses as status
import entity.status.player_statuses as p_status

class ChemicalOgre(m.Monster):
    def __init__(self,level):
        super(ChemicalOgre,self).__init__(level)
        self.health = self.level * 700
        self.power = self.level * 200
        self.action_points = 4
        self.base_ap = 4

    def do_turn(self):
        for a in self.statuses:
            a.do_turn()
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
        print 'the ogre roars and smashes the floor!'
        for player in self.owner.party.inventory:
            player.take_damage(self,self.power/3)

    def enrage(self):
        print 'the ogre is enraged, and has gotten stronger!'
        self.statuses.append(status.OgreEnrage())

    def autoattack(self):
		if self.action_points > 0:
			if not self.aggroed:
				self.select_aggro()

			if self.aggro.alive:
				self.attack(self.aggro)

    def feast(self):
        print 'the ogre eats an entire pig! where did it even get that??'
        self.health += (self.health * .2)

    def poison_splash(self):
        print 'the ogre pours a cask of poisonous sludge all over your party!'
        for player in self.owner.party.inventory:
            player.statuses.append(p_status.Poison(3,self.power * .1))
