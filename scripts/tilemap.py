class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            x_pos_1 = (3 + i) % 10
            y_pos_1 = 6 % 9

            self.tilemap[str(x_pos_1) + ';' + str(y_pos_1)] = {'type': 'block', 'variant': 0, 'pos': (x_pos_1, y_pos_1)}

            x_pos_2 = 6 % 10
            y_pos_2 = (3 + i) % 9

            self.tilemap[str(x_pos_2) + ';' + str(y_pos_2)] = {'type': 'block', 'variant': 0, 'pos': (x_pos_2, y_pos_2)}

    def render(self, surfc):
        for tile in self.offgrid_tiles:
            surfc.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surfc.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))