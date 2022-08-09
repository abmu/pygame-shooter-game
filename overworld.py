import pygame
from settings import *
from button import Button


class Overworld:
    def __init__(self,create_level):
        # general setup
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT,OW_FONT_SIZE)
        self.create_level = create_level

        # game title setup
        self.text_surf = self.font.render('SHOOTER GAME',False,OW_FONT_COLOUR)
        self.text_rect = self.text_surf.get_rect(center = (WIDTH/2-200,HEIGHT/2))

        # play button setup
        self.play_button = Button('Play',(WIDTH/2+200,HEIGHT/2),self.create_level)

    def run(self):
        # update and draw the overworld screen
        self.screen.blit(self.text_surf,self.text_rect)
        self.play_button.display()