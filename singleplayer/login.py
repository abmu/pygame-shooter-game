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
        self.line_setup()
        self.name_text = Text('Username',(WIDTH/2-350,HEIGHT/2-75))
        self.text_box = TextBox((WIDTH/2-350,HEIGHT/2-25))
        self.login_button = Button('LOGIN',(WIDTH/2-350,HEIGHT/2+35),self.create_animation)
        self.quit_button = Button('QUIT',(10,5),self.quit)

        # animation
        self.hide = False
        self.alpha = 255
        self.move = False
        self.end = False

        # title should accelerate to 10 speed when halfway, then deccelerate to 0 speed
        self.speed = 0
        self.distance = self.new_size[0] + 100 # 2 times the padding value
        self.start_pos = WIDTH/2+50
        self.acc_sign = -1 # negative acceleration
        self.acc_magnitude = 2/9 # calculated using SUVAT

    def create_animation(self):        
        # check if username is valid
        username = self.get_username()
        if not username.isspace() and len(username) > 0:
            self.hide = True

    def play_animation(self):
        if self.hide:
            # hide everything besides the title
            self.alpha -= 5
            self.line_image.set_alpha(self.alpha)
            self.name_text.set_alpha(self.alpha)
            self.text_box.set_alpha(self.alpha)
            self.login_button.set_alpha(self.alpha)
            self.quit_button.set_alpha(self.alpha)
            if self.alpha <= 0:
                self.hide = False
                self.move = True

        if self.move:
            # check if the title has reached the end pos
            if self.title_rect.topleft[0] == self.start_pos - self.distance:
                self.move = False
                self.end = True
            else:
                # check if the title is more than halfway across the distance it will travel
                if self.title_rect.topleft[0] <= self.start_pos - self.distance/2:
                    self.acc_sign = 1 # decelerate

                # move title
                self.speed += self.acc_sign * self.acc_magnitude
                self.title_rect.x += self.speed

        if self.end:
            self.end = False
            self.create_overworld()

    def title_setup(self):
        # scale down the title image
        image = pygame.image.load('graphics/title.png').convert_alpha()
        size = image.get_rect().size
        # make the scaled 2 times smaller
        self.new_size = (size[0]//2,size[1]//2) # (new width, new height)
        self.title_image = pygame.transform.scale(image, self.new_size)
        self.title_rect = self.title_image.get_rect(topleft = (WIDTH/2+50,HEIGHT/2-(self.new_size[1]/2)))

    def line_setup(self):
        # draw line next to title
        size = (4,self.new_size[1])
        pos = (WIDTH/2-size[0]/2,HEIGHT/2-size[1]/2)
        self.line_image = pygame.Surface(size).convert_alpha()
        self.line_image.fill('gray20')
        self.line_rect = self.line_image.get_rect(topleft = pos)

    def get_username(self):
        return self.text_box.get_text()

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self,event_list):
        # update and draw the login screen
        self.screen.blit(self.line_image,self.line_rect)
        self.name_text.display()
        self.text_box.display(event_list)
        self.screen.blit(self.title_image,self.title_rect)
        self.login_button.display()
        self.quit_button.display()
        self.play_animation()