import pygame
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from bullet import Bullet
from enemy import Enemy
from health_bar import HealthBar
from ui import UI


class Level:
    def __init__(self):
        # get display surface
        self.screen = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

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
                    self.weapon = Weapon(self.player.rect,[self.visible_sprites],self.visible_sprites.get_middle_pos())
                elif col == 'E':
                    enemy = Enemy((x,y),[self.visible_sprites,self.obstacle_sprites],self.obstacle_sprites)
                    HealthBar(enemy,[self.visible_sprites])

    def create_bullet(self,add_points):
        Bullet(self.weapon.get_pos(),[self.visible_sprites],self.obstacle_sprites,self.visible_sprites.get_middle_pos(),pygame.mouse.get_pos(),add_points)

    def run(self):
        # update and draw the level map and ui
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_width = self.screen.get_size()[0] // 2
        self.half_height = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def get_middle_pos(self):
        return (self.half_width,self.half_height)

    def draw(self,player):
        # get offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # sprites drawn later will be drawn on top
        # draw weapon on top of the tiles
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.draw_priority):
            # apply offset to each sprite
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image,offset_pos)

    def enemy_update(self,player):
        # give the enemy objects access to the player object
        enemy_sprites = [sprite for sprite in self.sprites() if sprite.__class__.__name__ == 'Enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)