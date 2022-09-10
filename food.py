import pygame
import random
from pygame import mixer
from settings import *


class Food(pygame.sprite.Sprite):
    def __init__(self,spawn_positions,groups,obstacle_sprites,sounds):
        # food setup
        super().__init__(groups)
        self.spawn_positions = spawn_positions
        self.last_pos = None
        self.image_1 = pygame.Surface((FOOD_SIZE,FOOD_SIZE)).convert_alpha()
        self.image_1.fill('deepskyblue1')
        self.image_2 = pygame.Surface((FOOD_SIZE,FOOD_SIZE)).convert_alpha()
        self.image_2.fill('lightskyblue1')
        self.image = self.image_1
        self.rect = self.image.get_rect(topleft = self.get_spawn_pos())
        self.drawn_mini = False
        self.draw_priority = 1

        # collision
        self.obstacle_sprites = obstacle_sprites

        # hit animation
        self.hit = False
        self.hit_cooldown = 100
        self.hit_time = None

        # stats
        self.health = 50

        # sound setup
        self.sounds = sounds

    def get_spawn_pos(self):
        # choose a random pos from the pickup pos dict
        # ensure that the pos is not taken and is not a None value
        spawn_pos = random.choice(list(self.spawn_positions.keys()))
        while self.spawn_positions[spawn_pos]: # self.spawn_positions[key] <- boolean value saying whether or not pos is currently taken
            spawn_pos = random.choice(list(self.spawn_positions.keys()))
            
        # make the previous pos occupied available and the current pos unavailable
        if self.last_pos is not None:
            self.spawn_positions[self.last_pos] = False
        self.spawn_positions[spawn_pos] = True
        self.last_pos = spawn_pos

        # ensure that the food is in the center of the square that they are on
        offset = (TILE_SIZE-FOOD_SIZE)/2
        return (spawn_pos[0]+offset,spawn_pos[1]+offset)

    def collision(self):
        # handle player collisions
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect): 
                if sprite.__class__.__name__ == 'Player':
                    # give points if player touches the food and make the food respawn
                    if not self.hit:
                        self.image = self.image_2
                        sprite.add_health(self.health)
                        sprite.increment_stat('Food')

                        # begin hit animation cooldown
                        self.hit = True
                        self.hit_time = pygame.time.get_ticks()
                        self.sounds.play('food_ping')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # check if hit animation cooldown has finished
        if self.hit:
            if current_time - self.hit_time >= self.hit_cooldown:
                self.hit = False
                self.image = self.image_1
                # make the food respawn
                self.rect.topleft = self.get_spawn_pos()

    def update(self):
        # update food
        self.cooldowns()
        self.collision()