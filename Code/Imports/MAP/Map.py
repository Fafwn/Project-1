import logging

logger = logging.getLogger(__name__)

tile_height = 0
tile_length = 0
tile_depth = 0
map = []


def change_dimensions(height, length, depth):
    return [[[0 for _ in range(length)] for _ in range(height)] for _ in range(depth)]



def display_map(map_data):
    for z in map_data:
        for y in z:
            for x in y:
                pass

map = change_dimensions(10, 10, 3)
display_map(map)
