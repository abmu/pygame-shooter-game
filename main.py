import pygame
import sys
from settings import *
from overworld import Overworld
from level import Level


class Game:
    def __init__(self):
        # pygame and screen setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Shooter Game')
        self.clock = pygame.time.Clock()

        self.status = "overworld"
        self.overworld = Overworld()
        # self.level = Level()

    def create_overworld(self):
        self.overworld = Overworld()
        self.status = "overworld"

    def create_level(self):
        self.level = Level()
        self.status = "level"

    def display_screen(self):
        # display the overworld screen or the level screen depending on whaat has happened in game
        if self.status == "overworld":
            self.overworld.run()
        else:
            self.level.run()

    def run(self):
        # game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # update screen
            self.screen.fill('black')
            self.display_screen()
            pygame.display.update()
            self.clock.tick(FPS)

# entry point
if __name__ == '__main__':
    game = Game()
    game.run()