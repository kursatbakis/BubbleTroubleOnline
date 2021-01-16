import pygame


class playerMovement:
    @staticmethod
    def updatePlayerPosition(player):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > player.speed:
            player.x -= player.speed
        if keys[pygame.K_RIGHT] and player.x + player.width + player.speed < 900 :
            player.x += player.speed
