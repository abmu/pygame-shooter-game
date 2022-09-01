import pygame
import random
from pygame import mixer
from settings import *


class Coin(pygame.sprite.Sprite):
    def __init__(self,spawn_positions,groups,obstacle_sprites,sounds):
        # coin setup
        super().__init__(groups)
        self.spawn_positions = spawn_positions
        self.last_pos = None
        self.image_1 = pygame.Surface((COIN_SIZE,COIN_SIZE)).convert_alpha()
        self.image_1.fill('goldenrod1')
        self.image_2 = pygame.Surface((COIN_SIZE,COIN_SIZE)).convert_alpha()
        self.image_2.fill('lightgoldenrod1')
        self.image = self.image_1
        self.rect = self.image.get_rect(topleft = self.get_spawn_pos())
        self.draw_priority = 1

        # collision
        self.obstacle_sprites = obstacle_sprites

        # hit animation
        self.hit = False
        self.hit_cooldown = 100
        self.hit_time = None

        # stats
        self.worth = 500

        # sound setup
        self.sounds = sounds

    def get_spawn_pos(self):
        # choose a random pos from the coin pos dict
        # ensure that the pos is not taken and is not a None value
        spawn_pos = random.choice(list(self.spawn_positions.keys()))
        while self.spawn_positions[spawn_pos]: # self.spawn_positions[key] <- boolean value saying whether or not pos is currently taken
            spawn_pos = random.choice(list(self.spawn_positions.keys()))
            
        # make the previous pos occupied available and the current pos unavailable
        if self.last_pos is not None:
            self.spawn_positions[self.last_pos] = False
        self.spawn_positions[spawn_pos] = True
        self.last_pos = spawn_pos

        return spawn_pos

    def collision(self):
        # handle player collisions
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect): 
                if sprite.__class__.__name__ == 'Player':
                    # give points if player touches the coin and make the coin respawn
                    if not self.hit:
                        self.image = self.image_2
                        sprite.add_points(self.worth)
                        sprite.increment_stat('Coins')

                        # begin hit animation cooldown
                        self.hit = True
                        self.hit_time = pygame.time.get_ticks()
                        self.sounds.play('coin_ping')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # check if hit animation cooldown has finished
        if self.hit:
            if current_time - self.hit_time >= self.hit_cooldown:
                self.hit = False
                self.image = self.image_1
                # make the coin respawn
                self.rect.topleft = self.get_spawn_pos()

    def update(self):
        # update coin
        self.cooldowns()
        self.collision()