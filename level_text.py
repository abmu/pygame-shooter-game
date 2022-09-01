import pygame
from settings import *


class LevelText(pygame.sprite.Sprite):
    def __init__(self,enemy_rect,get_level,groups):
        # level bar setup
        super().__init__(groups)
        self.font = pygame.font.Font(FONT_2,FONT_SIZE_2)
        self.enemy_rect = enemy_rect
        self.get_level = get_level
        self.setup_text()
        self.draw_priority = 2

    def setup_text(self):
        # get enemy level
        enemy_level = self.get_level()
        text = enemy_level[0]

        # create text 'image'
        self.image = self.font.render(f'{text}',True,COLOUR_2)
        self.rect = self.image.get_rect(center = self.get_pos())

    def get_pos(self):
        # make position of the level bar underneath the enemy
        return (self.enemy_rect.centerx,self.enemy_rect.centery)

    def update(self):
        # update enemy health bar
        self.setup_text()
        pos = self.get_pos()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]