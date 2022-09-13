import pygame
import sys
from settings import *
from network import Network

class Game:
    def __init__(self):
        # pygame and screen setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        icon = pygame.image.load(ICON)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        self.network = Network()
        self.player = self.network.get_p()

    def run(self):
        # game loop
        while True:
            sprites = self.network.send(self.player)

            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # update screen
            self.screen.fill('black')

            self.player.update(sprites)
            self.player.draw(self.screen)

            for sprite in sprites:
                sprite.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)

# entry point
if __name__ == '__main__':
    game = Game()
    game.run()