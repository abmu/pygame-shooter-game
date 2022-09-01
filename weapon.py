import pygame
from settings import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self,player_rect,groups,visible_sprites):
        # weapon setup
        super().__init__(groups)
        self.player_rect = player_rect
        self.middle_pos = visible_sprites.get_middle_pos()
        self.orig_image = pygame.Surface((WEAPON_X,WEAPON_Y)).convert_alpha()
        self.orig_image.fill('gray30')
        self.update()
        self.draw_priority = 3

    def set_direction(self):
        # calculate weapon direction vector
        mouse_pos = pygame.mouse.get_pos()
        self.direction = pygame.math.Vector2()
        self.direction.x = mouse_pos[0] - self.middle_pos[0]
        self.direction.y = mouse_pos[1] - self.middle_pos[1]

        # normalize direction vector to ensure it is a unit vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        else:
            # ensure the direction magnitude is not 0
            # else the weapon will be drawn on the player
            self.direction.x = 1
            self.direction.y = 0

        self.pos = (self.player_rect.centerx+self.direction.x*(PLAYER_SIZE//2+WEAPON_X//2), self.player_rect.centery+self.direction.y*(PLAYER_SIZE//2+WEAPON_X//2))

    def rotate(self):
        # rotate weapon about center by angle between unit vector i and self.direction
        angle = self.direction.angle_to(pygame.math.Vector2(1,0)) 
        self.image = pygame.transform.rotate(self.orig_image,angle)
        self.rect = self.image.get_rect(center = self.pos)

    def get_pos(self):
        # make start positon of bullet the end position of player weapon
        return (self.rect.centerx-BULLET_SIZE//2+self.direction.x*(WEAPON_X//2+BULLET_SIZE//2), self.rect.centery-BULLET_SIZE//2+self.direction.y*(WEAPON_X//2+BULLET_SIZE//2))

    def update(self):
        # update weapon
        self.set_direction()
        self.rotate()