import pygame
from settings import *


class PauseMenu:
    def __init__(self):
        # general setup
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT,UI_FONT_SIZE)

    def draW_pause_text(self):
        # draw points text
        text_surf = self.font.render('PAUSED',False,OW_FONT_COLOUR)
        text_rect = text_surf.get_rect(center = (WIDTH/2,HEIGHT/2))
        pygame.draw.rect(self.screen,'white',text_rect.inflate(100,200))
        self.screen.blit(text_surf,text_rect)

    def display(self):
        # update and draw pause menu
        self.draW_pause_text()