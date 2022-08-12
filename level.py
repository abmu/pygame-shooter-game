import pygame
from settings import *
from tile import Tile
from coin import Coin
from player import Player
from bullet import Bullet
from enemy import Enemy
from ui import UI


class Level:
    def __init__(self,create_overworld):
        # get display surface
        self.screen = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

        self.create_overworld = create_overworld

    def create_map(self):
        enemy_pos = {}
        coin_pos = {}
        for row_index, row in enumerate(MAP_ARRAY):
            for col_index, col in enumerate(row):
                # create sprites at correct positions
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
                elif col == 'P':
                    self.player = Player((x,y),[self.visible_sprites,self.obstacle_sprites],self.obstacle_sprites,self.visible_sprites,self.create_bullet)
                elif col == 'E':
                    enemy_pos[(x,y)] = False # ie. (x,y) position is not currently occupied
                elif col == 'C':
                    coin_pos[(x,y)] = False

        # the number of coins and enemies should be less than the number of possible positions
        # create enemy sprites in random enemy positions
        for count in range(len(enemy_pos)-1):
            Enemy(enemy_pos,[self.visible_sprites,self.obstacle_sprites],self.obstacle_sprites,self.visible_sprites)

        # create coin sprites in random coin positions
        for count in range(len(coin_pos)-1):
            Coin(coin_pos,[self.visible_sprites,self.obstacle_sprites],self.obstacle_sprites)

    def create_bullet(self,add_points):
        Bullet(self.player.weapon.get_pos(),[self.visible_sprites],self.obstacle_sprites,self.visible_sprites.get_middle_pos(),pygame.mouse.get_pos(),add_points)

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