import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,middle_pos,mouse_pos):
        # bullet setup
        super().__init__(groups)
        self.image = pygame.image.load('graphics/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        # movement
        self.set_direction(middle_pos,mouse_pos)
        self.speed = 0.5

        self.obstacle_sprites = obstacle_sprites

    def set_direction(self,middle_pos,mouse_pos):
        # calculate bullet direction vector
        self.direction = pygame.math.Vector2()
        self.direction.x = mouse_pos[0] - middle_pos[0]
        self.direction.y = mouse_pos[1] - middle_pos[1]

        # normalize direction vector to ensure it is a unit vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def move(self,speed):
        # store accourate position values in self.pos_x and self.pos_y
        # self.rect.x and self.rect.y will round values
        self.pos_x += self.direction.x * speed
        self.pos_y += self.direction.y * speed

        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

    def update(self):
        # update bullet
        self.move(self.speed)