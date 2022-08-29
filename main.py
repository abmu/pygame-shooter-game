import pygame
import sys
from pygame import mixer
from settings import *
from overworld import Overworld
from level import Level
from sounds import Sounds

class Game:
    def __init__(self):
        # pygame and screen setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Shooter Game')
        icon = pygame.image.load(ICON)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        # sound setup
        mixer.music.load('audio/8-bit-Monsters.mp3')
        self.sounds = Sounds()

        # default game screen
        self.create_overworld()

    def create_overworld(self):
        self.overworld = Overworld(self.create_level,self.sounds)
        self.status = 'overworld'

    def create_level(self):
        self.level = Level(self.create_overworld,self.sounds)
        self.status = 'level'
        mixer.music.play(-1)

    def display_screen(self):
        # display the overworld screen or the level screen depending on what has happened in game
        if self.status == 'overworld':
            self.screen.fill('white')
            self.overworld.run()
        else:
            self.screen.fill('black')
            self.level.run()

    def run(self):
        # game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # update screen
            self.display_screen()
            pygame.display.update()
            self.clock.tick(FPS)

# entry point
if __name__ == '__main__':
    game = Game()
    game.run()