import pygame
from settings import *


class Floor(pygame.sprite.Sprite):
    def __init__(self,pos,groups,size):
        # tile setup
        super().__init__(groups)
        self.image = pygame.Surface(size).convert_alpha()
        self.image.fill(COLOUR_2)
        self.rect = self.image.get_rect(topleft = pos)
        self.draw_priority = 0