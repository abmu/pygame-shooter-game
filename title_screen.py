import pygame
import sys
from settings import *
from text import Text
from button import Button


class TitleScreen:
    def __init__(self,create_level,create_settings):
        # general setup
        self.screen = pygame.display.get_surface()
        self.create_level = create_level
        self.create_settings = create_settings

        # title, text and buttons setup
        self.title_setup()
        self.name_text = Text('Name: ',(WIDTH/2+50,HEIGHT/2-OW_FONT_SIZE*3+10),'big')
        self.points_text = Text('Total Points: ',(WIDTH/2+50,HEIGHT/2-OW_FONT_SIZE*2+20),'big')
        self.play_button = Button('PLAY',(WIDTH/2+50,HEIGHT/2+10),self.create_level)
        self.settings_button = Button('SETTINGS',(WIDTH/2+50,HEIGHT/2+OW_FONT_SIZE+20),self.create_settings)
        self.quit_button = Button('QUIT',(10,5),self.quit)

    def title_setup(self):
        # scale down the title image
        image = pygame.image.load('graphics/title.png').convert_alpha()
        size = image.get_rect().size
        # make the scaled 2 times smaller
        new_size = (size[0]//2,size[1]//2) # (new width, new height)
        self.title_image = pygame.transform.scale(image, new_size)
        self.title_rect = self.title_image.get_rect(topleft = (WIDTH/2-400,HEIGHT/2-(new_size[1]/2)))

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        # update and draw the title screen
        self.screen.blit(self.title_image,self.title_rect)
        self.name_text.display()
        self.points_text.display()
        self.play_button.display()
        self.settings_button.display()
        self.quit_button.display()