import pygame
from settings import *
from title_screen import TitleScreen
from settings_screen import SettingsScreen


class Overworld:
    def __init__(self,create_level,create_login,sounds,username):
        # general setup
        self.create_level = create_level
        self.create_login = create_login
        self.sounds = sounds
        self.username = username
        self.create_title()

    def create_title(self):
        self.title_screen = TitleScreen(self.create_level,self.create_settings,self.create_login,self.username)
        self.status = 'title'

    def create_settings(self):
        self.settings_screen = SettingsScreen(self.create_title,self.sounds)
        self.status = 'options'

    def run(self):
        # update and draw the overworld
        if self.status == 'title':
            self.title_screen.run()
        else:
            self.settings_screen.run()