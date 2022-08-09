import pygame
from settings import *


class HealthBar(pygame.sprite.Sprite):
    def __init__(self,enemy_rect,get_health,groups):
        # health bar setup
        super().__init__(groups)
        self.enemy_rect = enemy_rect
        self.get_health = get_health
        self.set_bar_dimensions()
        self.rect = self.image.get_rect(topleft = self.get_pos())
        self.draw_priority = 2

    def set_bar_dimensions(self):
        # calculate current to max health ratio
        enemy_health = self.get_health()
        ratio = enemy_health[0] / enemy_health[1]

        # make new health bar image
        self.image = pygame.Surface((40*ratio,10))
        self.image.fill('red')

    def get_pos(self):
        # make position of the health bar underneath the enemy
        return (self.enemy_rect.centerx-20,self.enemy_rect.centery+30)

    def update(self):
        # update enemy health bar
        self.set_bar_dimensions()
        pos = self.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]