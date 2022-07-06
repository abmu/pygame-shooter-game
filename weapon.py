import pygame
from settings import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self,player_rect,groups,middle_pos):
        # weapon setup
        super().__init__(groups)
        self.player_rect = player_rect
        self.middle_pos = middle_pos
        self.orig_image = pygame.image.load('graphics/pistol.png').convert_alpha()
        self.update()

    def set_direction(self):
        # calculate weapon direction vector
        mouse_pos = pygame.mouse.get_pos()
        self.direction = pygame.math.Vector2()
        self.direction.x = mouse_pos[0] - self.middle_pos[0]
        self.direction.y = mouse_pos[1] - self.middle_pos[1]

        # normalize direction vector to ensure it is a unit vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def rotate(self):
        # rotate weapon about center by angle between unit vector i and self.direction
        angle = self.direction.angle_to(pygame.math.Vector2(1,0)) 
        self.image = pygame.transform.rotate(self.orig_image,angle)
        self.rect = self.image.get_rect(center = self.player_rect.center)

    def get_pos(self):
        # make start positon of bullet the end position of player weapon
        return (self.rect.centerx-8 + self.direction.x*64,self.rect.centery-8 + self.direction.y*64)

    def update(self):
        # update weapon
        self.set_direction()
        self.rotate()