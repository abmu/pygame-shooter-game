import pygame
from settings import *


class Overworld:
    def __init__(self):
        # general setup
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT,OW_FONT_SIZE)

    def draw_text(self):
        # draw text
        text_surf = self.font.render('SHOOTER GAME',False,OW_FONT_COLOUR)
        text_rect = text_surf.get_rect(center = (WIDTH/2-100,HEIGHT/2))
        self.screen.blit(text_surf,text_rect)

    def run(self):
        # update and draw the overworld screen
        self.draw_text()