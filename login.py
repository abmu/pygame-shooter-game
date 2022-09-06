import pygame
import sys
from settings import *
from text import Text
from button import Button
from text_box import TextBox


class Login:
    def __init__(self,create_overworld):
        # general setup
        self.screen = pygame.display.get_surface()
        self.create_overworld = create_overworld

        # title, text and buttons setup
        self.title_setup()
        self.name_text = Text(f'Username',(WIDTH/2+50,HEIGHT/2-75))
        self.text_box = TextBox((WIDTH/2+50,HEIGHT/2-25))
        self.login_button = Button('LOGIN',(WIDTH/2+50,HEIGHT/2+35),self.create_overworld)
        self.quit_button = Button('QUIT',(10,5),self.quit)

    def title_setup(self):
        # scale down the title image
        image = pygame.image.load('graphics/title.png').convert_alpha()
        size = image.get_rect().size
        # make the scaled 2 times smaller
        self.new_size = (size[0]//2,size[1]//2) # (new width, new height)
        self.title_image = pygame.transform.scale(image, self.new_size)
        self.title_rect = self.title_image.get_rect(topright = (WIDTH/2,HEIGHT/2-(self.new_size[1]/2)))

    def get_username(self):
        return self.text_box.get_text()

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self,event_list):
        # update and draw the login screen
        self.screen.blit(self.title_image,self.title_rect)
        self.name_text.display()
        self.text_box.display(event_list)
        self.login_button.display()
        self.quit_button.display()