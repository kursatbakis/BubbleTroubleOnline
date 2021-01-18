from projectile import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.width = 25
        self.height = 37
        self.speed = 10
        self.projectile = Projectile(self)
        self.hb = (self.x, self.y, 23, 37)
        self.lives = 5

    def shoot(self):
        if self.projectile.alive is False:
            self.projectile = Projectile(self)
            self.projectile.alive = True
