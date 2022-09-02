import pygame
from pygame import mixer
from settings import *
from text import Text
from button import Button
from slider import Slider


class SettingsScreen:
    def __init__(self,create_title,sounds):
        # general setup
        self.screen = pygame.display.get_surface()
        self.create_title = create_title
        self.escape_pressed = False

        # text and buttons setup
        self.music_text = Text('Music',(WIDTH/2-380,HEIGHT/2-190))
        self.music_slider = Slider(mixer.music,(WIDTH/2-205,HEIGHT/2-180))
        self.volume_text = Text('Volume',(WIDTH/2-380,HEIGHT/2-130))
        self.volume_slider = Slider(sounds,(WIDTH/2-205,HEIGHT/2-130))
        self.controls_text = Text('Controls',(WIDTH/2-380,HEIGHT/2-70))
        self.create_controls()
        self.back_button = Button('BACK',(10,5),self.create_title)

    def create_controls(self):
        # controls text setup
        self.keys = []
        self.actions = []
        for i, control in enumerate(CONTROLS):
            key = control[0]
            act = control[1]
            self.keys.append(Button(key,(WIDTH/2-205,HEIGHT/2-70+(i*40)),self.blank))
            self.actions.append(Text(act,(WIDTH/2+45,HEIGHT/2-70+(i*40))))

    def blank(self):
        # button function placeholder
        pass

    def input(self):
        keys = pygame.key.get_pressed()

        # go back to title screen
        if keys[pygame.K_ESCAPE]:
            self.escape_pressed = True
        else:
            if self.escape_pressed:
                self.create_title()
                self.escape_pressed = False

    def run(self):
        # update and draw the settings screen
        self.input()
        self.music_text.display()
        self.music_slider.display()
        self.volume_text.display()
        self.volume_slider.display()
        self.controls_text.display()
        for key in self.keys:
            key.display()
        for act in self.actions:
            act.display()
        self.back_button.display()