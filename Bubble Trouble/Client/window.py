import pygame
import pygame_menu
import sys
import time
import clientNetwork
from player import Player
from motor import BubbleGame
from Utility import Utility
from threading import Thread

pygame.init()
pygame.display.set_caption('BUBBLE TROUBLE ONLINE')

surface = pygame.display.set_mode((800, 600))
username = 'default'
playerSpeed = 2.4
clock = pygame.time.Clock()
player1 = Player(16, 560, 'character.png')
player2 = Player(200,560, 'character.png')
gameRunning = True
ballPos = (400, 100)
utility = Utility(ballPos, surface, (800, 600))
background = pygame.image.load('level1.png')
character_img = pygame.image.load('character.png')
playerId = -1
withId = -1
rivalUsername = 'empty'
port_game = 1
isMatchFound = False


def gameLoop():
    global surface
    character_x = 100
    character_y = 560
    while True:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print('ff')
        if keys[pygame.K_ESCAPE]:
            print('esc')
        if keys[pygame.K_LEFT]:
            print('left')
            character_x -= playerSpeed
        if keys[pygame.K_RIGHT]:
            print('right')
            character_x += playerSpeed

        surface.blit(background, (0,0))
        surface.blit(character_img, (character_x, character_y))
        pygame.display.update()


def draw_window():
    surface.blit(background, (0, 0))
    if player1.lives > 0:
        surface.blit(player1.projectile.image, (player1.projectile.x, player1.projectile.y))
        surface.blit(player1.image, (player1.x, player1.y))
    #also show player2
    utility.move_ball(player1.projectile, player2.projectile)
    if len(utility.balls) == 0:
        print('no balls left.')

    player1.hb = (player1.x, player1.y, 23, 37)
    player2.hb = (player2.x, player2.y, 23, 37)
    for ball in utility.balls:
        ball.hb = (ball.x, ball.y, 80, 80)

    pygame.display.update()


def matchFound(name, port, w):
    global rivalUsername, port_game, withId, isMatchFound
    rivalUsername = name
    port_game = port
    withId = w
    isMatchFound = True
    


def setPlayerId(i):
    global playerId
    playerId = i


def wait_for_match():
    global surface, isMatchFound
    Thread(target=clientNetwork.listenByTcp, daemon=True).start()
    pleaseWaitDir = 1
    pleaseWaitX = 10
    pleaseWaitY = 40
    counter = 0
    font = pygame.font.SysFont('timesnewromanbold',35)
    textColor1 = (255, 0, 95)
    textColor2 = (10, 10, 10)
    img = pygame.image.load('please_wait.jpg')
    img = pygame.transform.scale(img, (400,300))
    t = font.render('Please wait...', True, (30,30,25))
    text = font.render('LOOKING FOR A MATCH!', True, textColor1)
    clientNetwork.send_connect_packet(username)

    while not isMatchFound:
        clock.tick(32)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        surface.fill((255,195,47))
        if counter % 90 <= 45:
            text = font.render('Looking for a match!', True, textColor1)
        else:
            text = font.render('Looking for a match!', True, textColor2)

        if pleaseWaitDir == 1:
            pleaseWaitX += 0.70
        else:
            pleaseWaitX -= 0.70

        if pleaseWaitX >= 600 or pleaseWaitX <= 10:
            pleaseWaitDir *= -1

        surface.blit(text, (250, 200))
        surface.blit(img, (200, 250))
        surface.blit(t, (pleaseWaitX, pleaseWaitY))
        counter += 1
        pygame.display.update()

    bgame = BubbleGame(surface, window_height, window_width)
    bgame.game_loop()


def textInputDidChange(value: str) -> None:
    global username
    username = value


menu = pygame_menu.Menu(height=600,
                        width=800,
                        theme=pygame_menu.themes.THEME_ORANGE,
                        title='Bubble Trouble')

menu.add_text_input('Name: ', onchange=textInputDidChange)
menu.add_button('Start', wait_for_match)
menu.add_button('Quit', pygame_menu.events.EXIT)
menu.add_image('bt.png', scale=(0.7, 0.7), scale_smooth=True)
if __name__ == '__main__':
    menu.mainloop(surface)