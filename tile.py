import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        # tile setup
        super().__init__(groups)
        self.image = pygame.image.load('graphics/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.draw_priority = 1