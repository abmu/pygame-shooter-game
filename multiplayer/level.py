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


class Level:
    def __init__(self,sounds,username):
        # general setup
        self.screen = pygame.display.get_surface()
        self.status = 'play'
        self.sounds = sounds
        self.username = username

        # sprite group and sprite setup
        self.visible_sprites = CameraGroup()
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

    def input(self):
        keys = pygame.key.get_pressed()

        # open pause menu
        if keys[pygame.K_ESCAPE]:
            self.pause_pressed = True
        else:
            if self.pause_pressed:
                self.create_pause()
                self.pause_pressed = False

    def create_pause(self):
        # pause game if the status is 'play'
        if self.status == 'play':
            self.pause_menu = PauseMenu(self.player.stats,self.username)
            self.status = 'pause'
            self.timer.pause()
            mixer.music.pause()
        # unpause game if the status is 'pause'
        else:
            self.status = 'play'
            self.timer.unpause()
            mixer.music.unpause()

    def create_over(self):
        self.game_over = GameOver(self.player.stats,self.username)
        self.status = 'over'
        self.timer.pause()
        mixer.music.pause()

    def run(self):
        # play game ie. let sprites move unless the game is paused or is over
        if self.status == 'over':
            # game over
            self.player.user_input = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.screen.fill('white')
            self.game_over.display()
        else:
            # allow player to pause/unpause if the game is not over
            self.input()

            # update and draw the level map and ui
            self.visible_sprites.draw(self.player)
            self.ui.display(self.player,self.timer,self.player.weapon)

            # game playing
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)

            # check if the game timer has finished
            if self.timer.is_finish():
                self.create_over()
            
            if self.status == 'pause':
                # game paused
                self.player.user_input = False
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.pause_menu.display()
            else:
                self.player.user_input = True


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
        enemy_sprites = [sprite for sprite in self.sprites() if sprite.__class__.__name__ in ('Enemy','BossEnemy')]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)