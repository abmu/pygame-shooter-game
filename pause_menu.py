import pygame
from settings import *
from text import Text
from button import Button


class PauseMenu:
    def __init__(self,create_overworld,stats):
        # general setup
        self.screen = pygame.display.get_surface()
        self.create_overworld = create_overworld
        self.stats = stats

        # text and button setup
        self.paused_text = Text('PAUSE MENU',(WIDTH/2-130,HEIGHT/2-125),'big')
        self.stats_text = Text('Stats: ',(WIDTH/2-130,HEIGHT/2-90),'big')
        self.back_button = Button('LEAVE GAME',(WIDTH/2,HEIGHT/2+100),self.create_overworld)

    def draw_rect(self):
        # draw background rectangle
        pygame.draw.rect(self.screen,'white',(WIDTH/2-250,HEIGHT/2-250,500,500))

    def draw_stats(self):
        i = 0
        for stat in self.stats:
            text = Text(f'{stat}: {self.stats[stat]}',(WIDTH/2-130,HEIGHT/2-55+(i*35)),'small')
            text.display()
            i += 1

    def display(self):
        # update and draw pause menu
        self.draw_rect()
        self.paused_text.display()
        self.stats_text.display()
        self.draw_stats()
        self.back_button.display()