import pygame
from settings import *


class ReloadBar(pygame.sprite.Sprite):
    def __init__(self,player_rect,get_attack_cooldown,groups):
        # reload bar setup
        super().__init__(groups)
        self.player_rect = player_rect
        self.get_attack_cooldown = get_attack_cooldown
        self.set_bar_dimensions()
        self.rect = self.image.get_rect(topleft = self.get_pos())
        self.draw_priority = 5

    def set_bar_dimensions(self):
        # calculate time weapon has been on cooldown to cooldown time ratio
        weapon_cooldown = self.get_attack_cooldown()
        ratio = weapon_cooldown[0] / weapon_cooldown[1]

        # make new reload bar image
        self.image = pygame.Surface((PLAYER_SIZE*ratio,10)).convert_alpha()
        self.image.set_alpha(128)
        self.image.fill('white')
        
    def get_pos(self):
        # make position of the reload bar underneath the player
        return (self.player_rect.centerx-PLAYER_SIZE//2,self.player_rect.centery+PLAYER_SIZE//2+10)

    def update(self):
        # update enemy health bar
        self.set_bar_dimensions()
        pos = self.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]