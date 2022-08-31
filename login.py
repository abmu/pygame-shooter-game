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
        self.name_text = Text(f'Username',(WIDTH/2-250,HEIGHT/2-60))
        self.text_box = TextBox((WIDTH/2-80,HEIGHT/2-57))
        self.login_button = Button('LOGIN',(WIDTH/2-45,HEIGHT/2+20),self.create_overworld)
        self.quit_button = Button('QUIT',(10,5),self.quit)

    def get_username(self):
        return self.text_box.get_text()

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self,event_list):
        # update and draw the login screen
        self.name_text.display()
        self.text_box.display(event_list)
        self.login_button.display()
        self.quit_button.display()