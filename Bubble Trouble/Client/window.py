import os
import pygame
import pygame_menu
from motor import BubbleGame

pygame.init()
#os.environ['SDL_VIDEO_CENTERED'] = '1'
window_height = 600
window_width = 800
#TODO: oyundaki hız verilerinin hepsi 800x600'e göre ayarlandı pencere boyutu 
#değişecekse oralarında tekrar elden geçmesi gerekiyor!!
surface = pygame.display.set_mode((window_width, window_height))

def start_the_game():
    global surface
    surface.fill((255,27,79))
    
    bgame = BubbleGame(surface, window_height, window_width)
    bgame.game_loop()
    

menu = pygame_menu.Menu(height=window_height,
                        width=window_width,
                        onclose = pygame_menu.events.DISABLE_CLOSE,
                        theme=pygame_menu.themes.THEME_ORANGE,
                        title='Bubble Trouble')

menu.add_text_input('Name: ')
menu.add_button('Start', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)
