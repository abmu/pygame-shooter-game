import pygame
from settings import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self,player_rect,groups):
        # weapon setup
        super().__init__(groups)
        self.player_rect = player_rect
        self.middle_pos = (WIDTH/2,HEIGHT/2)
        self.draw_priority = 4

        # stats
        # default weapon is assault rifle
        self.change_weapon('Assault rifle')
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
        else:
            # ensure the direction magnitude is not 0
            # else the weapon will be drawn on the player
            self.direction.x = 1
            self.direction.y = 0

        self.pos = (self.player_rect.centerx+self.direction.x*(PLAYER_SIZE//2+self.size[0]//2), self.player_rect.centery+self.direction.y*(PLAYER_SIZE//2+self.size[0]//2))

    def rotate(self):
        # rotate weapon about center by angle between unit vector i and self.direction
        angle = self.direction.angle_to(pygame.math.Vector2(1,0)) 
        self.image = pygame.transform.rotate(self.orig_image,angle)
        self.rect = self.image.get_rect(center = self.pos)

    def change_weapon(self,weapon):
        # change weapon to what is passed in
        self.weapon = weapon
        self.stats = WEAPON_STATS[weapon]
        self.size = self.stats['size']

        # create new weapon image
        self.orig_image = pygame.Surface(self.stats['size']).convert_alpha()
        self.orig_image.fill('gray30')

    def get_cooldown(self):
        return self.stats['cooldown']

    def get_weight(self):
        return self.stats['weight']

    def get_bullet_stats(self):
        return (self.stats['power'],self.stats['speed'],self.size[1])

    def get_pos(self):
        # make start positon of bullet the end position of player weapon
        bullet_size = self.size[1] # make bullet size the size of width of weapon
        return (self.rect.centerx-bullet_size//2+self.direction.x*(self.size[0]//2+bullet_size//2), self.rect.centery-bullet_size//2+self.direction.y*(self.size[0]//2+bullet_size//2))

    def update(self):
        # update weapon
        self.set_direction()
        self.rotate()