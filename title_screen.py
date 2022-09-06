import pygame
import sys
import csv
from settings import *
from text import Text
from button import Button


class TitleScreen:
    def __init__(self,create_level,create_settings,create_login,username):
        # general setup
        self.screen = pygame.display.get_surface()
        self.create_level = create_level
        self.create_settings = create_settings
        self.create_login = create_login
        self.username = username
        self.escape_pressed = False

        # title, text and buttons setup
        self.title_setup()
        self.name_text = Text(f'Name: {self.username}',(WIDTH/2+50,HEIGHT/2-80))
        self.points_text_setup()
        self.play_button = Button('PLAY',(WIDTH/2+50,HEIGHT/2+10),self.create_level)
        self.settings_button = Button('SETTINGS',(WIDTH/2+50,HEIGHT/2+50),self.create_settings)
        self.back_button = Button('LOGOUT',(10,5),self.create_login)
        self.quit_button = Button('QUIT',(10,45),self.quit)

    def title_setup(self):
        # scale down the title image
        image = pygame.image.load('graphics/title.png').convert_alpha()
        size = image.get_rect().size
        # make the scaled 2 times smaller
        self.new_size = (size[0]//2,size[1]//2) # (new width, new height)
        self.title_image = pygame.transform.scale(image, self.new_size)
        self.title_rect = self.title_image.get_rect(topright = (WIDTH/2,HEIGHT/2-(self.new_size[1]/2)))

    # def draw_line(self):
    #     # draw line next to title
    #     pos = (self.title_rect.x+self.new_size[0],self.title_rect.y)
    #     size = (5,self.new_size[1])
    #     rect = pygame.Rect(pos,size)
    #     pygame.draw.rect(self.screen,'red',rect)

    def points_text_setup(self):
        found = False
        empty = True
        points = 0
        f_names = ['USERNAME','POINTS','GAMESPLAYED']
        # open the details.csv file
        # line format [USERNAME,POINTS,GAMESPLAYED]
        with open('details.csv','a+') as f:
            f.seek(0)
            reader = csv.DictReader(f)
            # iterate over each line in file
            for line in reader:
                # if the file is not empty the program will enter this for loop
                empty = False
                if line['USERNAME'] == self.username:
                    found = True
                    points = line['POINTS']
                    break

            # setup file if it is empty
            if empty:
                writer = csv.DictWriter(f,fieldnames=f_names)
                writer.writeheader()              

            # add new user to file if it doesn't already exist
            if not found:
                writer = csv.DictWriter(f,fieldnames=f_names)
                writer.writerow({'USERNAME':self.username,'POINTS':points,'GAMESPLAYED':0})

        self.points_text = Text(f'Total Points: {points}',(WIDTH/2+50,HEIGHT/2-40))

    def quit(self):
        pygame.quit()
        sys.exit()

    def input(self):
        keys = pygame.key.get_pressed()

        # go back to login screen
        if keys[pygame.K_ESCAPE]:
            self.escape_pressed = True
        else:
            if self.escape_pressed:
                self.create_login()
                self.escape_pressed = False

    def run(self):
        # update and draw the title screen
        self.input()
        self.screen.blit(self.title_image,self.title_rect)
        self.name_text.display()
        self.points_text.display()
        self.play_button.display()
        self.settings_button.display()
        self.quit_button.display()
        self.back_button.display()