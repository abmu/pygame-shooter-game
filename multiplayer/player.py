import pygame
from settings import *


class Player:
    def __init__(self,id_num,pos):
        # player setup
        self.id_num = id_num
        self.colours = [(255,0,0),(0,255,0),(0,0,255),(255,255,0)]
        self.colour = self.colours[id_num]
        self.joined = False

        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.size = PLAYER_SIZE
        self.rect = (self.pos_x,self.pos_y,self.size,self.size)

        # movement
        self.speed = 5
        self.direction = pygame.math.Vector2()
        
    def input(self):
        keys = pygame.key.get_pressed()

        # change player direction
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if pygame.mouse.get_pressed()[0] and not self.joined:
            self.joined = True

    def move(self):
        # normalize direction vector to ensure it is a unit vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos_x += self.direction.x * self.speed
        self.pos_y += self.direction.y * self.speed
        self.rect = (round(self.pos_x),round(self.pos_y),self.size,self.size)

    def draw(self,screen):
        # draw player
        if self.joined:
            pygame.draw.rect(screen,self.colour,self.rect)

    def update(self,sprites):
        # update player
        self.input()
        self.move()