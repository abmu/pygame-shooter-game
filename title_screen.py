import pygame
import sys
from settings import *
from button import Button


class TitleScreen:
    def __init__(self,create_level,create_settings):
        # general setup
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT,OW_PRIMARY_FONT_SIZE)
        self.create_level = create_level
        self.create_settings = create_settings

        # game title setup
        self.text_surf = self.font.render('SHOOTER GAME',False,OW_FONT_COLOUR)
        self.text_rect = self.text_surf.get_rect(center = (WIDTH/2-200,HEIGHT/2))

        # play button setup
        self.play_button = Button('PLAY',(WIDTH/2+200,HEIGHT/2-50),self.create_level)

        # settings button setup
        self.settings_button = Button('SETTINGS',(WIDTH/2+200,HEIGHT/2+50),self.create_settings)

        # quit button setup
        self.quit_button = Button('QUIT',(WIDTH-60,HEIGHT-25),self.quit)

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        # update and draw the title screen
        self.screen.blit(self.text_surf,self.text_rect)
        self.play_button.display()
        self.settings_button.display()
        self.quit_button.display()