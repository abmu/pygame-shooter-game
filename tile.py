import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        # tile setup
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE)).convert_alpha()
        self.image.fill('gray76')
        self.rect = self.image.get_rect(topleft = pos)
        self.draw_priority = 1