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
        self.colour = OW_FONT_COLOUR
        self.pos = pos
        self.slider_rect = pygame.Rect(self.pos,(450,15))

        self.volume = sound.get_volume()

    def draw_slider(self):
        # draw background bar
        pygame.draw.rect(self.screen,OW_SECONDARY_COLOUR,self.slider_rect)

        # draw current bar
        self.current_rect = self.slider_rect.copy()
        self.current_rect.width = self.slider_rect.width * self.volume
        pygame.draw.rect(self.screen,self.colour,self.current_rect)

    def draw_text(self):
        self.text = Text(str(round(self.volume*100)),(self.pos[0]+500,self.pos[1]-10),'big')
        self.text.display()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        # check if the mouse is touching the slider
        if self.slider_rect.collidepoint(mouse_pos) or self.current_rect.collidepoint(mouse_pos):
            self.colour = OW_PRIMARY_COLOUR
            # check if the left mouse button has been pressed
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.click_func(mouse_pos[0])
                    self.pressed = False
        else:
            self.colour = OW_FONT_COLOUR

    def click_func(self,mouse_pos):
        # calculate new volume from the position on the slider which was clicked
        rect_start_pos = self.pos[0]
        bar_pos_clicked = mouse_pos - rect_start_pos
        ratio = bar_pos_clicked / self.slider_rect.width

        # set volume to the ratio of the pos clicked on the bar and total width of bar
        self.volume = round(ratio,2)
        self.sound.set_volume(self.volume)

    def display(self):
        # update and draw slider and text
        self.draw_slider()
        self.draw_text()
        self.check_click()