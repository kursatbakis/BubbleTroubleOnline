import pygame
import pygame_menu
import sys
import time
import queue
import clientNetwork as cn
from motor import BubbleGame
from threading import Thread

pygame.init()
pygame.display.set_caption('BUBBLE TROUBLE ONLINE')

surface = pygame.display.set_mode((800, 600))
username = 'default'
clock = pygame.time.Clock()
playerId = -1
withId = -1
rivalUsername = 'empty'
match = False

def levelStart(rivallives, balls, noOfBalls, initialX, r_initialX, wait):
    pass

def matchFound(name, w):
    global rivalUsername, withId, match
    rivalUsername = name
    withId = w
    match = True
    print('Match!')

def forceEnd():
    pass

def setPlayerId(i):
    global playerId
    playerId = i

def rivalDied(remaining):
    pass

def wait_for_match():
    Thread(target=cn.listenByTcp, daemon=True).start()
    Thread(target=cn.listenByUdp, daemon=True).start()

    global surface, match
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
    while not match:
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
