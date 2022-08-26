import pygame
from settings import *


class Text:
    def __init__(self,text,pos,size):
        # general setup
        self.screen = pygame.display.get_surface()
        if size == 'big':
            self.font = pygame.font.Font(FONT_2,OW_FONT_SIZE)
        else:
            self.font = pygame.font.Font(FONT,UI_FONT_SIZE)

        # text setup
        self.text = text
        self.pos = pos
        self.text_surf = self.font.render(self.text,False,OW_FONT_COLOUR)
        self.text_rect = self.text_surf.get_rect(topleft = self.pos)

    def display(self):
        # update and draw text
        self.screen.blit(self.text_surf,self.text_rect)

