import unittest, math, inspect, base, sys
import dungeon.dungeon as d
# player imports
import entity.player.players as player
import entity.player.player_inventory as player_inv
import entity.ability.player_abilities as player_abilities
# item imports
import entity.item.armor as armor
import entity.item.weapon as weapon
import entity.item.consumable as consumable
import entity.item.items as items
import entity.item.controller as control
import entity.item.weapon_modification as item_mods
import entity.item.armor_modification as armor_mods
import entity.item.utils as utils
import entity.modifier
import entity.item.spell as spell
# monster imports
import entity.monster.monster_modification as monster_mods
import entity.monster.monsters as monsters
import entity.monster.bosses as boss
# statuses
import entity.status.player_statuses as statuses
# other
import entity.thing
import entity.chest
import StringIO as string


# experimental save testing yo
try:
    import dill
    dill_support = True
except:
    dill_support = False

class SaveTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pickle(self):
        self.player = player.Player('test',{'race':'Tank','attributes':{
            'agility': 2,
            'intelligence': 5,
            'strength': 8,
            'luck': 3,
            'mana': 0
        }})

        # ch = string.StringIO()
        ch = dill.dumps(self.player)
        self.clone = dill.loads(ch)
        self.assertEquals(self.clone.attributes, self.player.attributes)


class DungeonTest(unittest.TestCase):
    def setUp(self):
        self.dung = d.Dungeon(10,4,None)

    def tearDown(self):
        self.dung = None

    def test_size(self):
        size = 0
        for a in self.dung.rooms:
            for b in a:
                size += 1
        self.assertEquals(size,100)

class PlayerTest(unittest.TestCase):
    def setUp(self):
        base.INSTRUCTION_QUEUE = []
        base.IS_TEST = True
        self.party = player.Party()
        self.player = player.Player('john was here',{'race':'Tank','attributes':{
            'agility': 2,
            'intelligence': 5,
            'strength': 8,
            'luck': 3,
            'mana': 0
        }})
        self.party.add_player(self.player)
        self.dung = d.Dungeon(10,4,self.party)

    def tearDown(self):
        base.INSTRUCTION_QUEUE = []
        self.party = None
        self.player = None

    def test_aoe(self):
        # the instruction queue has to be reversed in order to be usable, lol
        base.INSTRUCTION_QUEUE = ['bow','Launch Volley','examine'][::-1]
        bow = weapon.Bow(5)
        stat = item_mods.Rusty()
        bow.modifiers.append(stat)
        self.player.inventory.append(bow)
        bow.equip()
        self.dung.rooms[0][0].things.clear()
        for a in range(6):
            spidey = monsters.Spider(1)
            weak = monster_mods.Weak()
            spidey.modifiers.append(weak)
            weak.apply()
            self.dung.rooms[0][0].things.append(spidey)
        self.party.current_dungeon = self.dung
        self.dung.start()
        self.party.handle_player_turn()


    def test_map(self):
        base.INSTRUCTION_QUEUE = ['open completed map','examine'][::-1]
        self.party.current_dungeon = self.dung
        self.player.inventory.append(utils.CompletedMap())
        self.dung.start()
        self.party.handle_player_turn()

    def test_carl(self):
        self.party.current_dungeon = self.dung
        self.dung.rooms[0][0].things.clear()
        # CORALLLLLL
        coral = boss.GrandMage(1)
        self.dung.rooms[0][0].things.append(coral)
        coral.room = self.dung.rooms[0][0]
        self.player.health = 100000
        self.dung.start()
        coral.cast_cosmicBlast()
        coral.cast_flood()
        coral.cast_restore()
        coral.cast_fireball()
        coral.cast_oops()

    def test_dragon(self):
        self.party.current_dungeon = self.dung
        self.dung.rooms[0][0].things.clear()
        # CORALLLLLL
        coral = boss.AncientDragon(1)
        self.dung.rooms[0][0].things.append(coral)
        coral.room = self.dung.rooms[0][0]
        self.player.health = 100000
        self.dung.start()
        coral.breathefire()
        # coral.fly()
        coral.sleep()
        coral.Roar()
        coral.autoattack()


    def test_armor(self):
        legs = armor.Platelegs(1)
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

    def test_armor_modifiers(self):
        legs = armor.Platelegs(2)
        begin = legs.armor

        mod = armor_mods.Good()
        legs.modifiers.append(mod)
        mod.apply()
        self.assertEquals(legs.armor,begin * 1.3)
        self.player.inventory.append(legs)
        legs.equip()

        self.assertEquals(self.player.armor,(legs.armor) + 1)

        self.player.take_damage(self.player,10,False)

    def test_armor_mods(self):
        for name, obj in inspect.getmembers(armor_mods):
            if inspect.isclass(obj):
                if name not in ['ModifyItems','Common','Uncommon','Rare','Legendary','Divined']: # divined will cause problems
                    self.setUp()
                    legs = armor.Platelegs(2)
                    mod = obj()
                    legs.modifiers.append(mod)
                    mod.apply()
                    self.player.inventory.append(legs)
                    legs.equip()
                    self.assertEquals(self.player.equipment['legs'],legs)
                    # base.put(name)
                    self.player.take_damage(self.player,30,False)
                    self.tearDown()

class AbilityTest(unittest.TestCase):
    def setUp(self):
        base.INSTRUCTION_QUEUE = []
        base.IS_TEST = True
        self.party = player.Party()
        self.player = player.Player('john was here',{'race':'Tank','attributes':{
            'agility': 2,
            'intelligence': 5,
            'strength': 8,
            'luck': 3,
            'mana': 0
        }})
        self.party.add_player(self.player)
        self.dung = d.Dungeon(10,4,self.party)
        self.player.inventory.clear()

    def tearDown(self):
        base.INSTRUCTION_QUEUE = []
        self.party = None
        self.player = None
        self.dung = None

    def test_ablities(self):
        for name, obj in inspect.getmembers(player_abilities):
            if inspect.isclass(obj):
                if name not in ['Ability','ShieldBash']:
                    self.setUp()
                    # we want the abilities to be able to proc
                    base.IS_TEST = False
                    for a in range(6):
                        spidey = monsters.Spider(1)
                        weak = monster_mods.Weak()
                        spidey.modifiers.append(weak)
                        weak.apply()
                        self.dung.rooms[0][0].things.append(spidey)
                    ability = obj()
                    self.player.inventory.append(ability)
                    self.party.current_dungeon = self.dung
                    base.put('========testing ability======== %s ' % ability)
                    self.dung.start()
                    self.party.handle_player_turn()
                    self.tearDown()
        self.setUp()
        self.player.attributes['mana'] = 5
        base.IS_TEST = False
        for a in range(6):
            spidey = monsters.Spider(1)
            weak = monster_mods.Weak()
            spidey.modifiers.append(weak)
            weak.apply()
            self.dung.rooms[0][0].things.append(spidey)
        sp = spell.SpellBook(2)
        self.player.inventory.append(player_inv.InventoryHandler())
        self.player.inventory.append(sp)
        sp.equip()
        self.party.current_dungeon = self.dung
        self.dung.start()
        self.party.handle_player_turn()


auto_tests = unittest.TestSuite()
auto_tests.addTests(unittest.TestLoader().loadTestsFromTestCase(DungeonTest))
auto_tests.addTests(unittest.TestLoader().loadTestsFromTestCase(PlayerTest))
if dill_support:
    auto_tests.addTests(unittest.TestLoader().loadTestsFromTestCase(SaveTest))


man_tests = unittest.TestSuite()
man_tests.addTests(unittest.TestLoader().loadTestsFromTestCase(AbilityTest))

# class WeaponMods(unittest.TestCase):
#     def setUp(self):
#         for a in inspect.getmembers(item_mods)




if __name__ == '__main__':
    # if you run the script without any arguments (like travis ci does) itll just run the automatic tests.
    # to test abilities and other things that require a little more finesse just specify any argument
    try:
        sys.argv[1]
        unittest.TextTestRunner().run(man_tests)
    except:
        unittest.TextTestRunner().run(auto_tests)
