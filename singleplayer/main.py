import pygame
import sys
from pygame import mixer
from settings import *
from login import Login
from overworld import Overworld
from level import Level
from sounds import Sounds


class Game:
    def __init__(self):
        # pygame and screen setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        icon = pygame.image.load(ICON)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        # sound setup
        mixer.music.load(MUSIC)
        mixer.music.set_volume(VOLUME) # initialise music volume to 1 (pygame sets it to ~0.99) 
        self.sounds = Sounds()

        # default game screen
        self.create_login()

    def create_login(self):
        self.login = Login(self.create_overworld)
        self.status = 'login'

    def create_overworld(self):
        username = self.login.get_username()
        self.overworld = Overworld(self.create_level,self.create_login,self.sounds,username)
        self.status = 'overworld'

    def create_level(self):
        self.level = Level(self.create_overworld,self.sounds,self.login.get_username())
        self.status = 'level'
        mixer.music.play(-1)

    def display_screen(self,event_list):
        # display the overworld screen or the level screen depending on what has happened in game
        if self.status == 'login':
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.screen.fill('white')
            self.login.run(event_list)
        elif self.status == 'overworld':
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.screen.fill('white')
            self.overworld.run()
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
            self.screen.fill('black')
            self.level.run()

    def run(self):
        # game loop
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # update screen
            self.display_screen(event_list)
            pygame.display.update()
            self.clock.tick(FPS)

# entry point
if __name__ == '__main__':
    game = Game()
    game.run()