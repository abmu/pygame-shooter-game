import pygame
from settings import *
from minimap import Minimap


class UI:
    def __init__(self,visible_sprites,map_size):
        # general setup
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT_2,FONT_SIZE_2)
        self.visible_sprites = visible_sprites

        # bar setup
        self.health_rect = pygame.Rect((20,20),(200,20))

        # minimap setup
        self.minimap = Minimap(visible_sprites,map_size)

    def draw_health_bar(self,player):
        # draw background bar
        pygame.draw.rect(self.screen,COLOUR_2,self.health_rect)

        # calculate current to max health ratio
        player_health = player.get_health()
        ratio = player_health[0] / player_health[1]

        # draw current health bar
        current_rect = self.health_rect.copy()
        current_rect.width = self.health_rect.width * ratio
        pygame.draw.rect(self.screen,'red',current_rect)
        
        # draw border bar
        pygame.draw.rect(self.screen,COLOUR_1,self.health_rect,2)

    def draw_points_text(self,player):
        # draw points text
        text_surf = self.font.render(f'POINTS: {player.stats["Points"]}',True,FONT_COLOUR_3)
        text_rect = text_surf.get_rect(topleft = (30,54))
        pygame.draw.rect(self.screen,COLOUR_2,text_rect.inflate(20,0))
        self.screen.blit(text_surf,text_rect)

    def draw_timer_text(self,timer):
        # draw timer text
        text_surf = self.font.render(f'{timer.get_timer_time()}',True,FONT_COLOUR_3)
        text_rect = text_surf.get_rect(topleft = (30,90))
        pygame.draw.rect(self.screen,COLOUR_2,text_rect.inflate(20,0))
        self.screen.blit(text_surf,text_rect)

    def display(self,player,timer):
        # update and draw ui
        self.draw_health_bar(player)
        self.draw_points_text(player)
        self.draw_timer_text(timer)
        self.minimap.display()