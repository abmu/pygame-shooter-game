import pygame
import sys
from pygame import mixer
from settings import *
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
        self.sounds = Sounds()

        # default game screen
        self.create_level()

    def create_level(self):
        self.level = Level(self.sounds,'Test')
        self.status = 'level'

    def run(self):
        # game loop
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # update screen
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

# entry point
if __name__ == '__main__':
    game = Game()
    game.run()