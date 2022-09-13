import pygame
from settings import *


class Tile:
    def __init__(self,pos):
        # tile setup
        self.colour = (191,191,191)

        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.size = TILE_SIZE
        self.rect = (self.pos_x,self.pos_y,self.size,self.size)

    def draw(self,screen):
        # draw tile
        pygame.draw.rect(screen,self.colour,self.rect)