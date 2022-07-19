import pygame
from settings import *


class HealthBar(pygame.sprite.Sprite):
    def __init__(self,enemy,groups):
        # health bar setup
        super().__init__(groups)
        self.enemy = enemy
        self.screen = pygame.display.get_surface()
        self.set_bar_dimensions()
        self.rect = self.image.get_rect(topleft = self.get_pos())

    def set_bar_dimensions(self):
        # calculate current to max health ratio
        ratio = self.enemy.health / self.enemy.max_health

        # destroy health bar if enemy dies
        if ratio <= 0:
            self.kill()

        # make new health bar image
        self.image = pygame.Surface((40*ratio,10))
        self.image.fill('red')

    def get_pos(self):
        # make position of the health bar underneath the enemy
        return (self.enemy.rect.centerx-20,self.enemy.rect.centery+30)

    def update(self):
        # update enemy health bar
        self.set_bar_dimensions()
        pos = self.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]