import pygame
from settings import *


class HealthBar(pygame.sprite.Sprite):
    def __init__(self,enemy_rect,get_health,groups):
        # health bar setup
        super().__init__(groups)
        self.enemy_rect = enemy_rect
        self.get_health = get_health
        self.size = ENEMY_SIZE
        self.set_bar_dimensions()
        self.rect = self.image.get_rect(topleft = self.get_pos())
        self.draw_priority = 3

    def set_bar_dimensions(self):
        # calculate current to max health ratio
        enemy_health = self.get_health()
        ratio = enemy_health[0] / enemy_health[1]

        # make new health bar image
        self.image = pygame.Surface((self.size*ratio,10)).convert_alpha()
        self.image.fill('red')
        
    def get_pos(self):
        # make position of the health bar underneath the enemy
        return (self.enemy_rect.centerx-self.size//2,self.enemy_rect.centery+self.size//2+10)

    def change_rect(self,rect,get_health,BOSS_SIZE):
        # change the rect that the health bar is attached to
        self.enemy_rect = rect
        self.get_health = get_health
        self.size = BOSS_SIZE

    def update(self):
        # update enemy health bar
        self.set_bar_dimensions()
        pos = self.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]