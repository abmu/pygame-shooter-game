import pygame
from settings import *


class BossBullet(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,vector,boss_rect):
        # bullet setup
        super().__init__(groups)
        # stats
        self.power = 34
        self.speed = 10

        self.vector = vector
        self.boss_rect = boss_rect # rect of the boss enemy that shot bullet
        orig_image = pygame.Surface((BOSS_BULLET_SIZE,BOSS_BULLET_SIZE)).convert_alpha()
        orig_image.fill('olivedrab1')
        orig_rect = orig_image.get_rect(topleft = pos)
        self.set_direction()
        self.rotate(orig_image,orig_rect)
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.drawn_mini = False
        self.draw_priority = 3

        # movement
        self.obstacle_sprites = obstacle_sprites

    def set_direction(self):
        # set boss bullet direction vector
        self.direction = self.vector

        # normalize direction vector to ensure it is a unit vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def rotate(self,image,rect):
        # rotate boss bullet about center by angle between unit vector i and self.direction
        angle = self.direction.angle_to(pygame.math.Vector2(1,0)) 
        self.image = pygame.transform.rotate(image,angle)
        self.rect = self.image.get_rect(center = rect.center)

    def move(self,speed):
        # store accourate position values in self.pos_x and self.pos_y
        # self.rect.x and self.rect.y will truncate values
        self.pos_x += self.direction.x * speed
        self.pos_y += self.direction.y * speed

        self.rect.x = round(self.pos_x)
        self.rect.y = round(self.pos_y)
        self.collision()

    def collision(self):
        # handle wall collisions
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.__class__.__name__ in ('Tile'):
                    self.kill()
                elif sprite.__class__.__name__ in ('Enemy','BossEnemy') and sprite.rect != self.boss_rect:
                    sprite.take_damage(self.power)
                    if sprite.is_dead():
                        sprite.update_stats(0)
                    self.kill()
                elif sprite.__class__.__name__ in ('Player'):
                    sprite.take_damage(self.power)
                    # if the player sprite dies update their stats
                    if sprite.is_dead():
                        sprite.update_stats()
                    self.kill()

    def update(self):
        # update boss bullet
        self.move(self.speed)