import pygame
import sys
import csv
from settings import *
from text import Text
from button import Button


class GameOver:
    def __init__(self,stats,username):
        # general setup
        self.screen = pygame.display.get_surface()
        self.escape_pressed = False
        self.stats = stats
        self.username = username
        self.update_points()

        # text and button setup
        self.over_setup()
        self.points_text = Text(f'Points earned: {self.stats["Points"]}',(WIDTH/2-450,HEIGHT/2-80))
        self.total_points_text = Text(f'Total points: {self.total_points}',(WIDTH/2-450,HEIGHT/2-40))
        self.back_button = Button('LEAVE GAME',(WIDTH/2-450,HEIGHT/2+50),self.quit)

    def quit(self):
        pygame.quit()
        sys.exit()

    def update_points(self):
        # read the old total points from the details.csv file
        with open('details.csv','r') as f:
            reader = csv.DictReader(f)
            lines = list(reader)

        # update the points for the user that was just playing
        for line in lines:
            if line['USERNAME'] == self.username:
                line['POINTS'] = int(line['POINTS']) + self.stats['Points']
                line['GAMESPLAYED'] = int(line['GAMESPLAYED']) + 1 # increment games played
                break

        self.total_points = line['POINTS']

        # write the updated total points to the file
        with open ('details.csv','w') as f:
            f_names = ['USERNAME','POINTS','GAMESPLAYED']
            writer = csv.DictWriter(f,fieldnames=f_names)
            writer.writeheader()
            writer.writerows(lines)

    def over_setup(self):
        # draw the game over text and lines
        self.over_image = pygame.image.load('../graphics/gameover.png').convert_alpha()
        size = self.over_image.get_rect().size
        self.over_rect = self.over_image.get_rect(topleft = (WIDTH/2-size[0]/2,HEIGHT/2-size[1]/2))

    def draw_stats(self):
        # draw the leaderboard numbers
        for i in range(8):
            num = Text(f'{i+1}',(WIDTH/2-60,HEIGHT/2-90+(i*35)))
            num.display()

        # draw player name
        name = Text(f'{self.username} (You)',(WIDTH/2+5,HEIGHT/2-90))
        name.display()

        # draw player stats
        i = 0
        for stat in self.stats:
            if stat not in ('Coins','Food'):
                text = Text(f'{self.stats[stat]}',(WIDTH/2+250+(i*85),HEIGHT/2-90))
                text.display()
                i += 1

    def input(self):
        keys = pygame.key.get_pressed()

        # go back to title screen
        if keys[pygame.K_ESCAPE]:
            self.escape_pressed = True
        else:
            if self.escape_pressed:
                self.create_overworld()
                self.escape_pressed = False

    def display(self):
        # update and draw game over screen
        self.input()
        self.screen.blit(self.over_image,self.over_rect)
        self.points_text.display()
        self.total_points_text.display()
        self.draw_stats()
        self.back_button.display()