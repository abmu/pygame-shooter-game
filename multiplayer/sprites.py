from settings import *
from player import Player
from tile import Tile


class Sprites:
    def __init__(self):
        # sprites setup
        self.s_list = []
        self.sprite_setup()

    def sprite_setup(self):
        id_num = 0
        for row_index, row in enumerate(MAP_ARRAY):
            for col_index, col in enumerate(row):
                # create sprites at correct positions
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    self.s_list.append(Tile((x,y)))
                elif col == 'P':
                    if id_num < PLAYER_COUNT:
                        self.s_list.append(Player(id_num,(x,y)))
                        id_num += 1

    def get_sprites(self,id_num):
        # return all sprites besides player specified
        s_copy = self.s_list.copy()
        for sprite in self.s_list:
            if sprite.__class__.__name__ == 'Player':
                if sprite.id_num == id_num:
                    s_copy.remove(sprite)
        return s_copy

    def get_player(self,id_num):
        # return player object
        for sprite in self.s_list:
            if sprite.__class__.__name__ == 'Player':
                if sprite.id_num == id_num:
                    return sprite

    def update_player(self,id_num,data):
        # update player object
        for s_index, sprite in enumerate(self.s_list):
            if sprite.__class__.__name__ == 'Player':
                if sprite.id_num == id_num:
                    self.s_list[s_index] = data