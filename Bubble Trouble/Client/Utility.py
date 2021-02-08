import pygame
from Ball import Ball

class Utility:
    def __init__(self, ballPosition, screen, windowSize):
        self.ballPosition = ballPosition
        self.screen = screen
        (self.width, self.height) = windowSize
        self.bg_color = (255, 255, 255)
        self.balls = []

    def init_ball(self, noOfBalls, size, amplitude, img, remCollisions):
        img = pygame.transform.scale(img, (size, size))

        for i in range(noOfBalls):
            if i % 2 == 0:
                ballPath = 1
            else:
                ballPath = -1

            ball = Ball(self.ballPosition, self.screen, (self.width, self.height), size, amplitude,
                        remCollisions, img)
            ball.speed = 16.0
            ball.angle = 2*ballPath

            self.balls.append(ball)

    def move_ball(self, projectile1, projectile2):
        for (index, ball) in enumerate(self.balls):
            ball.move()
            ball.bounce()
            isCollision = ball.collision(projectile1, projectile2)
            image = ball.image
            if isCollision[0] and ball.remCollisions > 0: #collisionTime: how many remaining collisions available for this ball
                size = ball.size
                amplitude = ball.amplitude
                remainingCollisions = ball.remCollisions
                self.ballPosition = (ball.x, ball.y)

                self.ball_projectile_collision(isCollision[1], index, projectile1, projectile2)
                self.init_ball(2, remainingCollisions, size, amplitude, image)
                self.move_ball(projectile1, projectile2)
            elif isCollision[0] and ball.remCollisions == 0:
                self.ball_projectile_collision(isCollision[1], index, projectile1, projectile2)

            ball.display(image)

        pygame.display.flip()

    def remove_ball(self, index):
        del self.balls[index]

    def ball_projectile_collision(self, onPlayer, index, projectile1, projectile2):
        self.remove_ball(index)

        if onPlayer == 1:
            projectile1.alive = False
            projectile1.x = -20
            projectile1.y = 0
            projectile1.hb = (projectile1.x, projectile1.y, 8, 480)
        else:
            projectile2.alive = False
            projectile2.x = -20
            projectile2.y = 0
            projectile2.hb = (projectile2.x, projectile2.y, 8, 480)
