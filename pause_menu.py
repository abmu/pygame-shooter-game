import pygame
from settings import *
from text import Text
from button import Button


class PauseMenu:
    def __init__(self,create_overworld,stats,username):
        # general setup
        self.screen = pygame.display.get_surface()
        self.create_overworld = create_overworld
        self.stats = stats
        self.username = username

        # text and button setup
        self.pause_setup()
        self.back_button = Button('LEAVE GAME',(WIDTH/2+130,HEIGHT/2+265),self.create_overworld)

    def pause_setup(self):
        # draw the pause menu text and lines
        self.pause_image = pygame.image.load('graphics/pause.png').convert_alpha()
        size = self.pause_image.get_rect().size
        self.pause_rect = self.pause_image.get_rect(topleft = (WIDTH/2-size[0]/2,HEIGHT/2-250))

    def draw_rect(self):
        # draw transparent background rectangle
        rect = pygame.Surface((700,650))
        rect.set_alpha(240)
        rect.fill('white')
        self.screen.blit(rect,(WIDTH/2-350,HEIGHT/2-325))

    def draw_points_text(self):
        # draw points earned text
        text = Text(f'Points earned: {self.stats["Points"]}',(WIDTH/2+25,HEIGHT/2-257))
        text.display()

    def draw_stats(self):
        # draw the leaderboard numbers
        for i in range(8):
            num = Text(f'{i+1}',(WIDTH/2-245,HEIGHT/2-55+(i*35)))
            num.display()

        # draw player name
        name = Text(f'{self.username} (You)',(WIDTH/2-180,HEIGHT/2-55))
        name.display()

        # draw player stats
        i = 0
        for stat in self.stats:
            if stat != 'Coins':
                text = Text(f'{self.stats[stat]}',(WIDTH/2+65+(i*85),HEIGHT/2-55))
                text.display()
                i += 1

    def display(self):
        # update and draw pause menu
        self.draw_rect()
        self.screen.blit(self.pause_image,self.pause_rect)
        self.draw_points_text()
        self.draw_stats()
        self.back_button.display()