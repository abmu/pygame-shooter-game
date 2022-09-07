import pygame
from settings import *


class TileMini(pygame.sprite.Sprite):
    def __init__(self,groups,sprite,map_size,multiplier):
        # mini tile setup
        super().__init__(groups)
        self.sprite = sprite
        self.map_size = map_size
        self.image = pygame.Surface((TILE_MINI_SIZE*multiplier,TILE_MINI_SIZE*multiplier)).convert_alpha()
        self.image.fill(self.get_colour())
        self.rect = self.image.get_rect(topleft = self.get_pos())
        self.draw_priority = 4

    def get_colour(self):
        # change colour depending on what the sprite is
        name = self.sprite.__class__.__name__
        if name =='Player':
            return 'red1'
        elif name =='Enemy':
            return 'green1'
        elif name == 'BossEnemy':
            return 'olivedrab1'
        elif name =='Bullet':
            return 'red4'
        elif name == 'BossBullet':
            return 'olivedrab4'
        elif name == 'Coin':
            return 'goldenrod1'
        elif name == 'Food':
            return 'deepskyblue1'
        else:
            # tile sprite
            return 'gray30'

    def get_pos(self):
        # move the mini sprite on the map
        rect_x = ((self.sprite.rect.x // TILE_SIZE) * TILE_MINI_SIZE) + 20
        rect_y = (HEIGHT - self.map_size[1] + ((self.sprite.rect.y // TILE_SIZE) * TILE_MINI_SIZE)) - 20
        return (rect_x,rect_y)

    def check_exist(self):
        # delete tile if the original sprite no longer exists
        if not self.sprite.alive():
            self.kill()

    def update(self):
        # update mini tile
        self.check_exist()
        pos = self.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]