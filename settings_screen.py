import pygame
from settings import *
from button import Button


class SettingsScreen:
    def __init__(self,create_title):
        # general setup
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT,OW_SECONDARY_FONT_SIZE)
        self.create_title = create_title

        # back button setup
        self.back_button = Button('BACK',(WIDTH/2+200,HEIGHT/2-50),self.create_title)

    def run(self):
        # update and draw the settings screen
        self.back_button.display()