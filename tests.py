import unittest, math
import dungeon.dungeon as d
import entity.player.players as p
import entity.item.armor as a

class DungeonTest(unittest.TestCase):
    def setUp(self):
        self.dung = d.Dungeon(20,4,None)

    def tearDown(self):
        self.dung = None

    def test_size(self):
        size = 0
        for a in self.dung.rooms:
            for b in a:
                size += 1
        self.assertEquals(size,400)

class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.party = p.Party()
        self.player = p.Player('john was here',{'race':'Dwarf','attributes':{
            'agility': 2,
            'intelligence': 5,
            'strength': 8,
            'luck': 3,
            'mana': 0
        }})
        self.party.add_player(self.player)

    def tearDown(self):
        self.party = None
        self.player = None

    def test_armor(self):
        legs = a.Platelegs(2)
        self.player.inventory.append(legs)
        legs.equip()

        self.assertEquals(self.player.armor,legs.armor + 1)

        start = self.player.health
        damage = 10

        self.player.take_damage(self.player,damage,False)
        # this should be the value of the armor
        self.assertEquals(round((start - self.player.health)),round(damage - (damage * ((25 * math.log(1+12+1, 11) + 3) / 100.0))))

        start = self.player.health
        legs.unequip()

        self.assertEquals(self.player.armor,1)

        self.player.take_damage(self.player,damage)
        self.assertEquals(round(start - self.player.health),round(damage - (damage * ((25 * math.log(1+1, 11) + 3) / 100.0))))


if __name__ == '__main__':
    unittest.main()
