import base, random
import entity.monster.monsters as m
import entity.status.monster_statuses as status
import entity.status.player_statuses as p_status
import entity.monster.monster_modification as mods
import math

class ChemicalOgre(m.Monster):
    def __init__(self,level):
        super(ChemicalOgre,self).__init__(level)
        self.health = self.level * 700
        self.max_health = self.level * 700
        self.power = math.pow(self.level * 80,1.05)
        self.action_points = 4
        self.base_ap = 4
        self.animals = 'horse cow sheep giraffe anteater anchovie dolphin dog cat antelope hippo whale'.split(' ')
        self.compute_rewards()

    def do_turn(self):
        for a in self.statuses:
            a.do_turn(None)
        if self.check_if_alive():
            self.owner.things.remove(self)

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
                base.put("the ogre looks around, apparently confused.")
        # base.put(self.health)

        self.action_points -= 1

    def smash(self):
        self.reveal()
        base.put('the ogre roars and smashes the floor!')
        for player in self.owner.party.inventory:
            player.take_damage(self,self.power/3)

    def enrage(self):
        self.reveal()
        base.put('the ogre is enraged, and has gotten stronger!')
        self.statuses.append(status.OgreEnrage())

    def autoattack(self):
        self.reveal()
        if self.action_points > 0:
            if not self.aggroed:
                self.select_aggro()
            if self.aggro.alive:
                self.attack(self.aggro)
            else:
                self.select_aggro()
                self.attack(self.aggro)


    def feast(self):
        self.reveal()
        base.put('the ogre eats an entire %s!! where did it even get that??' % random.choice(self.animals))
        self.health += (self.max_health * .05)

    def poison_splash(self):
        self.reveal()
        base.put('the ogre pours a cask of poisonous sludge all over your party!')
        for player in self.owner.party.inventory:
            player.statuses.append(p_status.Poison(3,self.power * .1))

    def to_str(self):
        return "She'rak the Chemical Ogre"

class AncientDragon(m.Monster):
    def __init__(self,level):
        super(AncientDragon,self).__init__(level)
        self.health = self.level * 1000
        self.max_health = self.level * 1000
        self.power = self.level*75
        self.action_points = 1
        self.base_ap = 1
        self.compute_rewards()


    def do_turn(self):
        for a in self.statuses:
            a.do_turn(None)
        self.check_if_alive()

        if self.action_points > 0:
            roll = base.D6.roll()
            if roll is 1:
                self.breathefire()
            if roll is 3:
                self.sleep()
            if roll is 4:
                self.Roar()
            if roll is 5 or roll is 6 or roll is 2:
                self.autoattack()
        #base.put(self.health)

        self.action_points -= 1

    def breathefire(self):
        self.reveal()
        base.put('Zearth breathes a sea of fire at his enemies!')
        for player in self.owner.party.inventory:
            roll=base.D20.roll()
            if roll<12:
                player.take_damage(self,self.power/3)
                player.statuses.append(p_status.Burn(math.ceil(self.level/4),self.power/(self.level/2.0)))
            else:
                base.put('%s has dodged the flames!' %player.name)

    def autoattack(self):
        self.reveal()
        if self.action_points > 0:
            if not self.aggroed:
                self.select_aggro()
            if self.aggro.alive:
                self.attack(self.aggro)
            else:
                self.select_aggro()
                self.attack(self.aggro)


    def Roar(self):
        self.reveal()
        base.put('Zearth lets loose a mighty roar terrifying everyone!')
        for player in self.owner.party.inventory:
            player.statuses.append(p_status.Maim(math.ceil(self.level/4),1))

    def sleep(self):
        self.reveal()
        base.put('Zearth locks eyes with one in the party and sends them into a deep sleep')
        if self.action_points > 0:
            if not self.aggroed:
                self.select_aggro()
            if self.aggro.alive:
                self.aggro.statuses.append(p_status.Sleep())
            else:
                self.select_aggro()
                self.agro.statuses.append(p_status.Sleep())

    def to_str(self):
        return "Zearth the Elder Dragon"

class SpiderQueen(m.Monster):
    def __init__(self,level):
        super(SpiderQueen,self).__init__(level)
        self.health = self.level * 400
        self.power = self.level * 100
        self.compute_rewards()


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
        base.put("the spider queen births %d new spiderlings!" % num)
        for a in range(num):
            self.owner.things.append(m.Spiderling(self.level))

    def autoattack(self):
        self.reveal()
        if self.action_points > 0:
            if not self.aggroed:
                self.select_aggro()

            if self.aggro.alive:
                self.attack(self.aggro)
                self.aggro.statuses.append(p_status.Poison(5,self.power/8))
            else:
                self.select_aggro()
                self.attack(self.aggro)
                self.aggro.statuses.append(p_status.Poison(5,self.power/8))

    def to_str(self):
        return "Araknai the Spider Queen"

class GrandMage(m.Monster):
    def __init__(self,level):
        super(GrandMage,self).__init__(level)
        self.health = self.level * 200
        self.power = self.level * 40
        self.max_health=self.level * 200
        self.compute_rewards()


    def do_turn(self):
        for a in self.statuses:
            a.do_turn(None)
        self.check_if_alive()

        if self.action_points > 0:
            roll = base.D20.roll()
            if roll >= 20:
                self.cast_cosmicBlast()
            elif roll>=18:
                self.cast_flood()
            elif roll>=13:
                self.cast_restore()
            elif roll>=7:
                self.cast_fireball()
            else:
                self.cast_oops()


        self.action_points -= 1

    def attack(self,target,damage):
        self.reveal()
        target.take_damage(self,damage)
        self.take_damage(target,target.retaliate())

    def cast_fireball(self):
        self.reveal()
        roll=base.D6.roll()
        base.put("Carl summons a mass of fire!")
        if self.action_points > 0:
            if not self.aggroed:
                self.select_aggro()

            if self.aggro.alive:
                self.attack(self.aggro,self.power)
                self.aggro.statuses.append(p_status.Burn(math.ceil(roll/2),self.power/8*roll))
            else:
                self.select_aggro()
                self.attack(self.aggro,self.power)
                self.aggro.statuses.append(p_status.Burn(math.ceil(roll/2),self.power/8*roll))

    def cast_flood(self):
        self.reveal()
        base.put("Carl closes his eyes and starts to chant. The room quickly fills with water!")
        for a in self.owner.party.inventory:
            self.attack(a,self.power)

    def cast_restore(self):
        self.reveal()
        base.put("The elements form around Carl and heal him!")
        if self.action_points > 0:
            self.health=self.max_health

    def cast_cosmicBlast(self):
        num=0
        for a in self.owner.things:
            if isinstance(a,m.Monster):
                a.conceal()
                num+=1
        self.conceal()
        base.put("The rooms is plunged into darkness as a all light is gathered into a ball")
        base.put("Carl seems to have disappeared along with all other monsters!")
        if self.action_points > 0:
            if not self.aggroed:
                self.select_aggro()

            if self.aggro.alive:
                self.attack(self.aggro,self.power*(2+num))
                self.aggro.statuses.append(p_status.Stun(base.D3.roll()))
                self.aggro.statuses.append(p_status.Burn(base.D3.roll(),num*(self.power/5)))
            else:
                self.select_aggro()
                self.attack(self.aggro,self.power*(2+num))
                self.aggro.statuses.append(p_status.Burn(base.D3.roll(),num*(self.power/5)))
                self.aggro.statuses.append(p_status.Stun(base.D3.roll()))

    def cast_oops(self):
        self.reveal()
        base.put("Carl seems to have missed invokation!")

    def to_str(self):
        return "Carl the Grand Magus"

boss_options = [ChemicalOgre, SpiderQueen, GrandMage, AncientDragon]
