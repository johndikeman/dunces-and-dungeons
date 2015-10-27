import unittest
import dungeon.dungeon as d
import entity.player.players as p

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

class ArmorTest(unittest.TestCase):
    def setUp(self):
        self.party = p.Party()
        self.player = p.Player({'race':'Dwarf'})

if __name__ == '__main__':
    unittest.main()
