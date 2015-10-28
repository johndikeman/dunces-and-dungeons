import unittest, math, inspect, base
import dungeon.dungeon as d
# player imports
import entity.player.players as player
import entity.player.player_inventory as player_inv
# item imports
import entity.item.armor as armor
import entity.item.weapon as weapon
import entity.item.consumable as consumable
import entity.item.items as items
import entity.item.controller as control
import entity.item.item_modification as item_mods
# monster imports
import entity.monster.monster_modification as monster_mods
import entity.monster.monsters as monsters
# statuses
import entity.status.player_statuses as statuses
# other
import entity.thing
import entity.chest


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
        self.party = player.Party()
        self.player = player.Player('john was here',{'race':'Dwarf','attributes':{
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
        legs = armor.Platelegs(2)
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

        self.player.take_damage(self.player,damage,False)
        self.assertEquals(round(start - self.player.health),round(damage - (damage * ((25 * math.log(1+1, 11) + 3) / 100.0))))

# class WeaponMods(unittest.TestCase):
#     def setUp(self):
#         for a in inspect.getmembers(item_mods)


if __name__ == '__main__':
    unittest.main()
