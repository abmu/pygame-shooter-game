import pygame
from settings import *


class Floor(pygame.sprite.Sprite):
    def __init__(self,pos,groups,size):
        # tile setup
        super().__init__(groups)
        self.image = pygame.image.load('graphics/floor.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft = pos)
        self.draw_priority = 0