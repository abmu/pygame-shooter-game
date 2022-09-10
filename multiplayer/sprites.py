import pygame
from settings import *
from pygame import mixer
from tile import Tile
from floor import Floor
from player import Player
from bullet import Bullet
from timer import Timer
from ui import UI
from pause_menu import PauseMenu
from game_over import GameOver


class Sprites:
    def __init__(self,sounds,username):
        # general setup
        self.screen = pygame.display.get_surface()
        self.status = 'play'
        self.sounds = sounds
        self.username = username

        # sprite group and sprite setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

        # user interface
        self.ui = UI(self.visible_sprites,self.map_size)
        self.timer = Timer(GAME_LENGTH)
        self.pause_pressed = False

    def create_map(self):
        player_pos = {}
        enemy_pos = {}
        pickup_pos = {}
        for row_index, row in enumerate(MAP_ARRAY):
            for col_index, col in enumerate(row):
                # create sprites at correct positions
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
                elif col == 'P':
                    player_pos[(x,y)] = False # ie. (x,y) position is not currently occupied
                elif col == 'E':
                    enemy_pos[(x,y)] = False
                elif col == 'C':
                    pickup_pos[(x,y)] = False

        self.map_size = (x,y)
        Floor((0,0),[self.visible_sprites],self.map_size)

        self.player = Player(player_pos,[self.visible_sprites,self.obstacle_sprites],self.obstacle_sprites,self.visible_sprites,self.create_bullet,self.sounds)

    def create_bullet(self,add_points,increment_stat,get_bullet_stats):
        Bullet(self.player.weapon.get_pos(),[self.visible_sprites],self.obstacle_sprites,self.visible_sprites,add_points,increment_stat,get_bullet_stats)