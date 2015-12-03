import entity.item.items as items


class CompletedMap(items.ItemUsedFromInventory):
    def __init__(self):
        super(CompletedMap,self).__init__()
        self.options = ['open completed map']
        # map will be the matrix
        self.map = []
        self.name = "a completed map of the dungeon"
        self.cost = 200

    def do_turn(self,arg):
        if arg is self.options[0]:
            self.map = []
            self.populate_map_matrix()
            # this is for brevity.
            rooms = self.owner.party.current_dungeon.rooms
            for row in range(len(rooms)):
                for col in range(len(rooms[row])):
                    # check first if there is a room at that position
                    if rooms[col][row]:
                        # check to see if theyre in the room
                        self.map[col][row] = 'R '
                        if rooms[col][row].contains_chest():
                            self.map[col][row] = 'C '
                        if rooms[col][row].cords == self.owner.party.current_dungeon.active_room.cords:
                            self.map[col][row] = 'X '
                        if rooms[col][row].contains_exit():
                            self.map[col][row] = 'L '
            base.put(self.format_output())

    def format_output(self):
        ret = '+-'
        for a in self.map[0]:
            ret += '--'
        ret += '+\n'
        for a in self.map:
            ret += '| '
            for b in a:
                ret += b
            ret += '|\n'
        ret += '+'
        for a in self.map[0]:
            ret += '--'
        ret += '-+\n'
        return ret

    def populate_map_matrix(self):
        for rowind,row in enumerate(self.owner.party.current_dungeon.rooms):
            self.map.append([])
            for colind,col in enumerate(row):
                self.map[rowind].append('  ')

class Map(CompletedMap):
    def __init__(self):
        super(Map,self).__init__()
        self.options = ['open map']
        self.name = 'a blank map'
        self.cost = 20

    def do_turn(self,arg):
        if arg is self.options[0]:
            self.map = []
            self.populate_map_matrix()
            # this is for brevity.
            rooms = self.owner.party.current_dungeon.rooms
            for row in range(len(rooms)):
                for col in range(len(rooms[row])):
                    # check first if there is a room at that position
                    if rooms[col][row] and rooms[col][row].entered:
                        # check to see if theyre in the room
                        self.map[col][row] = 'R '
                        if rooms[col][row].contains_chest():
                            self.map[col][row] = 'C '
                        if rooms[col][row].cords == self.owner.party.current_dungeon.active_room.cords:
                            self.map[col][row] = 'X '
                        if rooms[col][row].contains_exit():
                            self.map[col][row] = 'L '
            base.put(self.format_output())
