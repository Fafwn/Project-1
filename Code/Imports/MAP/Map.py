import logging

logger = logging.getLogger(__name__)

class MapArea:
    tile_height = 0
    tile_width = 0
    tile_depth = 0
    map = [[[]]]

    def __init__(self):
        self.change_dimensions(10, 10, 3)
        self.display_map()
        self.input_map(",".join([str(x) for x in range(200)]).split(","))
        self.display_map()


    def change_dimensions(self, height, width, depth):
        self.tile_height = height
        self.tile_width = width
        self.tile_depth = depth
        self.map = [[[0 for _ in range(width)] for _ in range(height)] for _ in range(depth)]


    def display_map(self):
        logger.info('\n'.join(f"\nLayer {layer}\n" + '-' * ((len(z) + 1) * 2) + "\n" + '\n'.join(
            ''.join(f'|{x}' for x in y) + '|' for y in z) + '\n' + '-' * ((len(z) + 1) * 2) for layer, z in
                        enumerate(self.map)))


    def input_map(self, new_data):
        for index, value in enumerate(new_data):
            x = index%10
            y = (index//10) - (index//100 * 10)
            z = index//100
            #print("X:%s\nY:%s\nZ:%s\n" % (x,y,z))
            self.map[z][y][x] = value



MapArea()