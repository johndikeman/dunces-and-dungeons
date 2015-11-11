import entity.item.items as items


class CompletedMap(items.ItemUsedFromInventory):
    def __init__(self):
        super(CompletedMap,self).__init__()
        self.options = ['open map']
        # map will be the matrix
        self.map = []

    def do_turn(self,arg):
        self.map = []
        self.populate_map_matrix()
        # this is for brevity.
        rooms = self.owner.party.current_dungeon.rooms
        if arg is self.options[0]:
            for row in range(len(rooms)):
                for col in range(len(rooms[row])):
                    # check first if there is a room at that position
                    if rooms[col][row]:
                        # check to see if theyre in the room
                        self.map[col][row] = 'R '
                        if rooms[col][row].cords == self.owner.party.current_dungeon.active_room.cords:
                            self.map[col][row] = 'X '
                        if rooms[col][row].contains_exit():
                            self.map[col][row] = 'L '
            ret = ''
            for a in self.map:
                for b in a:
                    ret += b
                ret += '\n'
            print ret

    def populate_map_matrix(self):
        for rowind,row in enumerate(self.owner.party.current_dungeon.rooms):
            self.map.append([])
            for colind,col in enumerate(row):
                self.map[rowind].append('  ')
