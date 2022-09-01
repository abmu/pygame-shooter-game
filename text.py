import pygame
from settings import *


class Text:
    def __init__(self,text,pos):
        # general setup
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT_1,FONT_SIZE_1)

        # text setup
        self.text = text
        self.pos = pos
        self.text_surf = self.font.render(self.text,True,FONT_COLOUR_1)
        self.text_rect = self.text_surf.get_rect(topleft = self.pos)

    def get_size(self):
        return self.font.size(self.text)

    def display(self):
        # update and draw text
        self.screen.blit(self.text_surf,self.text_rect)

