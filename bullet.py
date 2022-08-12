import pygame
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,middle_pos,mouse_pos,add_points):
        # bullet setup
        super().__init__(groups)
        orig_image = pygame.image.load('graphics/bullet.png').convert_alpha()
        orig_rect = orig_image.get_rect(topleft = pos)
        self.set_direction(middle_pos,mouse_pos)
        self.rotate(orig_image,orig_rect)
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.draw_priority = 3

        # movement
        self.obstacle_sprites = obstacle_sprites
        self.add_points = add_points

        # stats
        self.speed = 10
        self.power = 34

    def set_direction(self,middle_pos,mouse_pos):
        # calculate bullet direction vector
        self.direction = pygame.math.Vector2()
        self.direction.x = mouse_pos[0] - middle_pos[0]
        self.direction.y = mouse_pos[1] - middle_pos[1]

        # normalize direction vector to ensure it is a unit vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def rotate(self,image,rect):
        # rotate bullet about center by angle between unit vector i and self.direction
        angle = self.direction.angle_to(pygame.math.Vector2(1,0)) 
        self.image = pygame.transform.rotate(image,angle)
        self.rect = self.image.get_rect(center = rect.center)

    def move(self,speed):
        # store accourate position values in self.pos_x and self.pos_y
        # self.rect.x and self.rect.y will round values
        self.pos_x += self.direction.x * speed
        self.pos_y += self.direction.y * speed

        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.collision()

    def collision(self):
        # handle wall collisions
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.__class__.__name__ == 'Tile':
                    self.kill()
                elif sprite.__class__.__name__ == 'Enemy':
                    sprite.take_damage(self.power)
                    # if the enemy sprite dies and respawns, ie. their health regenerates, award the player a certain amount of points
                    if sprite.health == sprite.max_health:
                        self.add_points(sprite.get_worth())
                    self.kill()

    def update(self):
        # update bullet
        self.move(self.speed)