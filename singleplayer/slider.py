import pygame
from settings import *
from text import Text


class Slider:
    def __init__(self,sound,pos):
        # general setup
        self.screen = pygame.display.get_surface()
        self.pressed = False
        self.sound = sound

        # bar setup
        self.colour = COLOUR_2
        self.pos = pos
        self.slider_rect = pygame.Rect(self.pos,(500,15))

        self.volume = sound.get_volume()

    def draw_slider(self):
        # draw background bar
        pygame.draw.rect(self.screen,COLOUR_4,self.slider_rect)

        # draw current bar
        self.current_rect = self.slider_rect.copy()
        self.current_rect.width = self.slider_rect.width * self.volume
        pygame.draw.rect(self.screen,self.colour,self.current_rect)

    def draw_text(self):
        text = Text(str(round(self.volume*100)),(self.pos[0]+550,self.pos[1]-10))
        text.display()

    def check_hover(self):
        # change cursor to a hand if the cursor is hovering over the slider
        if self.slider_rect.collidepoint(pygame.mouse.get_pos()) or self.current_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        # check if the slider was pressed
        if self.pressed:
            self.colour = COLOUR_1
            # if the mouse button is still down move the slider
            if pygame.mouse.get_pressed()[0]:
                self.click_func(mouse_pos[0])
            else:
                self.pressed = False
        else:
            # check if the mouse is touching the slider
            if self.slider_rect.collidepoint(mouse_pos) or self.current_rect.collidepoint(mouse_pos):
                self.colour = COLOUR_1
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = True
            else:
                self.colour = COLOUR_2

    def click_func(self,mouse_pos):
        # calculate new volume from the position on the slider which was clicked
        rect_start_pos = self.pos[0]
        bar_pos_clicked = mouse_pos - rect_start_pos
        ratio = bar_pos_clicked / self.slider_rect.width

        # ensure ratio is between 1 and 0
        if ratio > 1:
            ratio = 1
        elif ratio < 0:
            ratio = 0

        # set volume to the ratio of the pos clicked on the bar and total width of bar
        self.volume = round(ratio,2)
        self.sound.set_volume(self.volume)

    def display(self):
        # update and draw slider and text
        self.draw_slider()
        self.draw_text()
        self.check_click()
        self.check_hover()