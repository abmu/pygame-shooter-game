import pygame
from settings import *
from text import Text
from button import Button


class GameOver:
    def __init__(self,create_overworld,stats):
        # general setup
        self.screen = pygame.display.get_surface()
        self.create_overworld = create_overworld
        self.stats = stats

        # text and button setup
        self.over_text = Text('GAME OVER',(WIDTH/2-130,HEIGHT/2-125),'small')
        self.stats_text = Text('STATS: KILLS/DEATHS/POINTS',(WIDTH/2-130,HEIGHT/2-90),'small')
        self.back_button = Button('BACK',(WIDTH/2+50,HEIGHT/2+100),self.create_overworld)

    def draw_rect(self):
        # draw background rectangle
        pygame.draw.rect(self.screen,'white',(WIDTH/2-200,HEIGHT/2-200,400,400))

    def display(self):
        # update and draw game over screen
        self.draw_rect()
        self.over_text.display()
        self.stats_text.display()
        self.back_button.display()