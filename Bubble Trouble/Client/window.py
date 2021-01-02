import os
import pygame
import pygame_menu

pygame.init()
#os.environ['SDL_VIDEO_CENTERED'] = '1'
surface = pygame.display.set_mode((800, 600))

def start_the_game():
    global surface
    surface.fill((255,27,79))
    



menu = pygame_menu.Menu(height=600,
                        width=800,
                        onclose = pygame_menu.events.DISABLE_CLOSE,
                        theme=pygame_menu.themes.THEME_ORANGE,
                        title='Bubble Trouble')

menu.add_text_input('Name: ')
menu.add_button('Start', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)