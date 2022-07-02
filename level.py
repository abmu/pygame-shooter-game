import pygame
from settings import *
from tile import Tile
from player import Player
from bullet import Bullet


class Level:
    def __init__(self):
        # get display surface
        self.screen = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(MAP_ARRAY):
            for col_index, col in enumerate(row):
                # create sprites at correct positions
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
                elif col == 'P':
                    self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_bullet)

    def create_bullet(self):
        Bullet((self.player.get_pos()),[self.visible_sprites],self.obstacle_sprites,self.visible_sprites.get_middle_pos(self.player),pygame.mouse.get_pos())

    def run(self):
        # update and draw the level map
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_width = self.screen.get_size()[0] // 2
        self.half_height = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def get_middle_pos(self,player):
        return (self.half_width,self.half_height)

    def draw(self,player):
        # get offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # apply offset to each sprite
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image,offset_pos)