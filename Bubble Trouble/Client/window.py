import pygame
import pygame_menu
import sys
import time
import clientNetwork
import player

pygame.init()
surface = pygame.display.set_mode((800, 600))
username = 'default'
playerSpeed = 2.4
clock = pygame.time.Clock()
player1 = player(16, 560, 'character.png')

def game(level):
    global surface
    background = pygame.image.load('level{}.png'.format(level))
    background = pygame.transform.scale(background, (800,600))
    character_img = pygame.image.load('character.png')
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
            pla
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


def send_match_request():
    print('send match request')


def wait_for_match():
    global surface
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
    send_match_request()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        surface.fill((255,195,47))
        if counter % 300 <= 150:
            text = font.render('Looking for a match!', True, textColor1)
        else:
            text = font.render('Looking for a match!', True, textColor2)

        if pleaseWaitDir == 1:
            pleaseWaitX += 0.08
        else:
            pleaseWaitX -= 0.08

        if pleaseWaitX >= 600 or pleaseWaitX <= 10:
            pleaseWaitDir *= -1

        surface.blit(text, (250, 200))
        surface.blit(img, (200, 250))
        surface.blit(t, (pleaseWaitX, pleaseWaitY))
        counter += 1
        pygame.display.update()


def textInputDidChange(value: str) -> None:
    global username
    username = value

menu = pygame_menu.Menu(height=600,
                        width=800,
                        theme=pygame_menu.themes.THEME_ORANGE,
                        title='Bubble Trouble')

menu.add_text_input('Name: ', onchange=textInputDidChange)
menu.add_button('Start', game, 1)
menu.add_button('Quit', pygame_menu.events.EXIT)
menu.add_image('bt.png', scale=(0.7, 0.7), scale_smooth=True)
#clientNetwork.send_connection(username)
if __name__ == '__main__':
    menu.mainloop(surface)