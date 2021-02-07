import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        self.image = pygame.image.load('arrow.png')
        self.x = player.x + 6
        self.y = player.y + 36
        self.speed = -10
        self.alive = False
        self.hb = (self.x, self.y, 8, 480)

    def update_projectile(self):
        if self.alive:
            if self.y + self.speed > 0:
                self.y += self.speed
                self.hb = (self.x, self.y, 8, 480)
            else:
                self.alive = False
                self.x = -20
                self.hb = (self.x, self.y, 8, 480)