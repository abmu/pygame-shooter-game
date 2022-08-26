import pygame
from settings import *
from text import Text
from button import Button


class PauseMenu:
    def __init__(self,create_overworld):
        # general setup
        self.screen = pygame.display.get_surface()
        self.create_overworld = create_overworld

        # text and button setup
        self.paused_text = Text('PAUSED',(WIDTH/2-130,HEIGHT/2-125),'small')
        self.stats_text = Text('STATS: KILLS/DEATHS/COINS/POINTS',(WIDTH/2-130,HEIGHT/2-90),'small')
        self.back_button = Button('BACK',(WIDTH/2+50,HEIGHT/2+100),self.create_overworld)

    def draw_rect(self):
        # draw background rectangle
        pygame.draw.rect(self.screen,'white',(WIDTH/2-150,HEIGHT/2-150,300,300))

    def display(self):
        # update and draw pause menu
        self.draw_rect()
        self.paused_text.display()
        self.stats_text.display()
        self.back_button.display()