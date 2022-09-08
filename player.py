import pygame
import pygame.gfxdraw
import random
from pygame import mixer
from settings import *
from weapon import Weapon
from reload_bar import ReloadBar


class Player(pygame.sprite.Sprite):
    def __init__(self,spawn_positions,groups,obstacle_sprites,visible_sprites,create_bullet,sounds):
        # player setup
        super().__init__(groups)
        self.spawn_positions = spawn_positions
        self.last_pos = None

        # setup default player image
        s = PLAYER_SIZE
        self.image_1 = pygame.Surface((s,s),pygame.SRCALPHA).convert_alpha()
        pygame.gfxdraw.aacircle(self.image_1,s//2,s//2,s//2-1,(255,0,0)) # red1 colour
        pygame.gfxdraw.filled_circle(self.image_1,s//2,s//2,s//2-1,(255,0,0))
        # setup player hit image image
        self.image_2 = pygame.Surface((s,s),pygame.SRCALPHA).convert_alpha()
        pygame.gfxdraw.aacircle(self.image_2,s//2,s//2,s//2-1,(139,0,0)) # red4 colour
        pygame.gfxdraw.filled_circle(self.image_2,s//2,s//2,s//2-1,(139,0,0))

        self.image = self.image_1
        self.rect = self.image.get_rect(topleft = self.get_spawn_pos())
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.drawn_mini = False
        self.draw_priority = 4

        # movement
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.visible_sprites = visible_sprites

        # shooting
        self.pressed = False
        self.create_bullet = create_bullet
        self.attacking = False
        self.attack_time = None

        # hit
        self.hit = False
        self.hit_cooldown = 100
        self.hit_time = None

        # stats
        self.max_health = 100
        self.health = self.max_health
        self.stats = {'Points':0,'Kills':0,'Deaths':0,'Coins':0,'Food':0}
        self.dead = False

        # weapons
        self.weapon = Weapon(self.rect,[self.visible_sprites],self.visible_sprites)
        self.update_speed()

        if RELOAD_BAR: # check if the reload bar is enabled in settings file
            self.reload_bar = ReloadBar(self.rect,self.get_attack_cooldown,[self.visible_sprites])

        # sound setup
        self.sounds = sounds

    def get_spawn_pos(self):
        # choose a random pos from the player pos dict
        # ensure that the pos is not taken or is the last pos and is not a None value
        spawn_pos = random.choice(list(self.spawn_positions.keys()))
        while self.spawn_positions[spawn_pos]: # self.spawn_positions[key] <- boolean value saying whether or not pos is currently taken
            spawn_pos = random.choice(list(self.spawn_positions.keys()))
            
        # make the previous pos occupied available and the current pos unavailable
        if self.last_pos is not None:
            self.spawn_positions[self.last_pos] = False
        self.spawn_positions[spawn_pos] = True
        self.last_pos = spawn_pos

        return spawn_pos

    def update_speed(self):
        # change speed depending on weapon selected
        self.min_speed = 5 - self.weapon.get_weight()
        self.max_speed = 7 - self.weapon.get_weight()
        self.speed = self.min_speed

    def update_stats(self):
        # update stats
        self.health = self.max_health
        # deduct points if the player dies
        self.add_points(-1000)
        self.increment_stat('Deaths')

        self.dead = False

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

        # make player move faster
        if keys[pygame.K_LSHIFT]:
            # gradually increase speed
            self.speed += 0.05
            if self.speed >= self.max_speed:
                self.speed = self.max_speed
        else:
            # gradually decrease speed
            self.speed -= 0.05
            if self.speed <= self.min_speed:
                self.speed = self.min_speed

        # change weapon
        if keys[pygame.K_1]:
            self.weapon.change_weapon('Pistol')
            self.update_speed()
        elif keys[pygame.K_2]:
            self.weapon.change_weapon('Assault rifle')
            self.update_speed()
        elif keys[pygame.K_3]:
            self.weapon.change_weapon('Sniper')
            self.update_speed()

        # shoot bullet
        if (pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]) and not self.attacking: # check if lmb clicked
            self.pressed = True
        else:
            if self.pressed:
                self.create_bullet(self.add_points,self.increment_stat,self.weapon.get_bullet_stats)
                self.sounds.play('shoot_ping')
                self.pressed = False

                # begin attack cooldown
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

    def move(self,speed):
        # normalize direction vector to ensure it is a unit vector
        # if direction vector is diagonal the magnitude > 1 <- not unit vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos_x += self.direction.x * speed
        self.rect.x = round(self.pos_x)
        self.collision('horizontal')
        self.pos_y += self.direction.y * speed
        self.rect.y = round(self.pos_y)
        self.collision('vertical')        

    def collision(self,direction):
        # handle horizontal collisons
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect) and sprite.__class__.__name__ in ('Tile','Enemy','BossEnemy'):
                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right
                    elif self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left
                    self.pos_x = self.rect.x

        # handle vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect) and sprite.__class__.__name__ in ('Tile','Enemy','BossEnemy'):
                    if self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom
                    elif self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                    self.pos_y = self.rect.y

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # check if attack cooldown has finished
        if self.attacking:
            if current_time - self.attack_time >= self.weapon.get_cooldown():
                self.attacking = False

        # check if hit cooldown has finished
        if self.hit:
            if current_time - self.hit_time >= self.hit_cooldown:
                self.hit = False
                self.image = self.image_1

    def get_attack_cooldown(self):
        # return the time the weapon has been on cooldown for and the total cooldown duration
        if self.attacking:
            current_time = pygame.time.get_ticks()
            return (current_time - self.attack_time, self.weapon.get_cooldown())
        return (0, self.weapon.get_cooldown())

    def take_damage(self,power):
        if not self.hit:
            # load hit image
            self.image = self.image_2
            self.sounds.play('hit_ping')

            # make the player take damage
            self.health -= power
            # check if the player is dead
            if self.health <= 0:
                # make the player respawn once they die
                self.image = self.image_1
                self.rect.topleft = self.get_spawn_pos()
                self.pos_x = self.rect.x
                self.pos_y = self.rect.y
                self.dead = True
                self.sounds.play('death_ping')
            else:
                # begin hit cooldown
                self.hit = True
                self.hit_time = pygame.time.get_ticks()

    def is_dead(self):
        return self.dead

    def get_health(self):
        return (self.health,self.max_health)

    def add_points(self,points):
        self.stats['Points'] += points
        if self.stats['Points'] <= 0:
            # set the points to 0 if their points goes below 0
            self.stats['Points'] = 0

    def add_health(self,health):
        # add health to the player
        self.health += health
        if self.health > self.max_health:
            self.health = self.max_health

    def increment_stat(self,stat):
        self.stats[stat] += 1

    def update(self):
        # update player
        self.input()
        self.cooldowns()
        self.move(self.speed)