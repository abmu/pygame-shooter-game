import pygame
from settings import *


class UI:
    def __init__(self):
        # general setup
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT,UI_FONT_SIZE)

        # bar setup
        self.health_rect = pygame.Rect(10,10,BAR_WIDTH,BAR_HEIGHT)

    def draw_health_bar(self,player):
        # draw background bar
        pygame.draw.rect(self.screen,UI_PRIMARY_COLOUR,self.health_rect)

        # calculate current to max health ratio
        player_health = player.get_health()
        ratio = player_health[0] / player_health[1]

        # draw current health bar
        current_rect = self.health_rect.copy()
        current_rect.width = self.health_rect.width * ratio
        pygame.draw.rect(self.screen,UI_HEALTH_COLOUR,current_rect)
        
        # draw border bar
        pygame.draw.rect(self.screen,UI_SECONDARY_COLOUR,self.health_rect,1)

    def draw_points_text(self,player):
        # draw points text
        text_surf = self.font.render('POINTS: ' + str(int(player.points)),False,UI_FONT_COLOUR)
        text_rect = text_surf.get_rect(topleft = (20,40))
        pygame.draw.rect(self.screen,UI_PRIMARY_COLOUR,text_rect.inflate(20,0))
        self.screen.blit(text_surf,text_rect)

    def draw_timer_text(self,timer):
        # draw timer text
        text_surf = self.font.render(f'{timer.get_timer_time()}',False,UI_FONT_COLOUR)
        text_rect = text_surf.get_rect(topleft = (20,75))
        pygame.draw.rect(self.screen,UI_PRIMARY_COLOUR,text_rect.inflate(20,0))
        self.screen.blit(text_surf,text_rect)

    def display(self,player,timer):
        # update and draw ui
        self.draw_health_bar(player)
        self.draw_points_text(player)
        self.draw_timer_text(timer)