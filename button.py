import pygame
from settings import *


class Button:
    def __init__(self,text,pos,func):
        # general setup
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT_2,FONT_SIZE_1)
        self.pressed = False
        self.func = func

        # text setup
        self.colour = FONT_COLOUR_1
        self.text = text
        self.pos = pos
        self.alpha = 255

    def draw_text(self):
        # draw the button text
        self.text_surf = self.font.render(self.text,True,self.colour)
        self.text_surf.set_alpha(self.alpha)
        self.text_rect = self.text_surf.get_rect(topleft = self.pos)
        self.screen.blit(self.text_surf,self.text_rect)

    def set_alpha(self,alpha):
        # change alpha
        self.alpha = alpha

    def check_hover(self):
        # change cursor to a hand if the cursor is hovering over the button
        if self.text_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        # check if the mouse is touching the text button
        if self.text_rect.collidepoint(mouse_pos):
            self.colour = FONT_COLOUR_2
            # check if the left mouse button has been pressed
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            # once the left mouse button has been let go then carry out the function of the button
            else:
                if self.pressed:
                    self.click_func()
                    self.pressed = False
        else:
            self.colour = FONT_COLOUR_1

    def click_func(self):
        # print('clicked!')
        self.func()

    def display(self):
        # update and draw button
        self.draw_text()
        self.check_click()
        self.check_hover()
