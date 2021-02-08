import math


class Ball:
    def __init__(self, x, y, windowSize, screen, size, amplitude, remCollisions, image):
        self.x = x
        self.y = y
        self.width, self.height = windowSize
        self.screen = screen
        self.size = size
        self.amplitude = amplitude
        self.image = image
        self.speed = 0
        self.angle = 0
        self.firstTouch = True
        self.remCollisions = remCollisions

    def display(self, image):
        self.screen.blit(image, (self.x, self.y))

    def move(self):
        self.x += (math.sin(self.angle) * self.speed) / self.amplitude
        self.y -= (math.cos(self.angle) * self.speed)

    def bounce(self):
        if self.x > self.width - self.size:  # bouncing from right
            self.x = 2 * (self.width - self.size) - self.x
            self.angle *= -1
        elif self.x < 1:  # bouncing from left
            if self.x < 0:
                self.x *= -2
            else:
                self.x *= 2

            self.angle *= -1

        if self.firstTouch is False and self.y <= self.height / 3:
            self.y = 3 * (self.height / 3 - 74) - self.y  # bu ne alaka anlamadim.. degistirilir
            self.angle = math.pi - self.angle

        if self.y + self.size > self.height:  # sagdan carpsa
            self.y = 2 * (self.height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.firstTouch = False
        elif self.y < 1:  # soldan carpsa
            self.y *= 2
            self.angle = math.pi - self.angle

    def collision(self, projectile1, projectile2):
        if self.y + self.size > projectile1.hb[1]:  # player1
            if self.x + self.size > projectile1.hb[0] and self.x < projectile1.hb[0] + projectile1.hb[2]:
                self.remCollisions -= 1
                self.size -= 10
                self.amplitude -= 1
                return True, 1

        if self.y + self.size > projectile2.hb[1]:  # player2
            if self.x + self.size > projectile2.hb[0] and self.x < projectile2.hb[0] + projectile2.hb[2]:
                self.remCollisions -= 1
                self.size -= 10
                self.amplitude -= 1
                return True, 2

        return False, 1
