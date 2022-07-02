import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_bullet):
        # player setup
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5

        # shooting
        self.pressed = False
        self.create_bullet = create_bullet

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        # change player direction
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # shoot bullet
        if pygame.mouse.get_pressed()[0]: # check if lmb clicked
            self.pressed = True
        else:
            if self.pressed:
                self.create_bullet()
                self.pressed = False

    def move(self,speed):
        # normalize direction vector to ensure it is a unit vector
        # if direction vector is diagonal the magnitude > 1 <- not unit vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')        

    def collision(self,direction):
        # handle horizontal collisons
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right
                    elif self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left

        # handle vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom
                    elif self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top

    def get_pos(self):
        # subtract half the bullet width and height
        # make bullet center start at player center
        return (self.rect.centerx-8,self.rect.centery-8)

    def update(self):
        # update player
        self.input()
        self.move(self.speed)