import pygame
import time
import random
import math

class BubbleGame:
    ######window
    #window_height = 600
    #window_width = 800
    #window_border_left
    #window_border_right
    #window_border_up
    #window_border_down

    #speeds
    player_speed_pixels = 5
    hook_speed_pixels = 15
    ball_speed_pixels = 3

    hit_jump_pixels = 50 #FIXME

    ######colors
    white = (255,255,255)
    black = (0,0,0)

    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

    bright_red = (255,155,155)
    bright_green = (155,255,155)
    bright_blue = (155,155,255)

    ########ball
    ball_array = []
    #fixme: ball_mutex
    ######

    clock = pygame.time.Clock()

    #####math
    pi_steps = 50
    top_step = pi_steps//2 #zirve noktası
    one_step_size = ((math.pi))/pi_steps

    #####images

    ballImg_red = pygame.image.load('Images/rball6.bmp')
    ballImg_orange = pygame.image.load('Images/orange_ball.gif')
    ballImg_yellow = pygame.image.load('Images/yellow_ball.gif')
    ballImg_green = pygame.image.load('Images/green_ball.gif')


    player_image_height = 37
    player_image_width = 23
    playerImg_1 = pygame.transform.scale(pygame.image.load('Images/player.png'), (player_image_width, player_image_height))
    playerImg_2 = pygame.transform.scale(pygame.image.load('Images/player2.png'), (player_image_width, player_image_height))

    arrowImg = pygame.image.load('Images/arrow.png')
    #####Ball levels
    size_lvl_8 = 135
    size_lvl_7 = 95
    size_lvl_6 = 70
    size_lvl_5 = 55
    size_lvl_4 = 40
    size_lvl_3 = 27
    size_lvl_2 = 18
    size_lvl_1 = 10
    ball_sizes = [size_lvl_1, size_lvl_2, size_lvl_3, size_lvl_4, size_lvl_5, size_lvl_6, size_lvl_7, size_lvl_8]

    high_lvl_8 = 350
    high_lvl_7 = 270
    high_lvl_6 = 220
    high_lvl_5 = 180
    high_lvl_4 = 150
    high_lvl_3 = 125
    high_lvl_2 = 100
    high_lvl_1 = 80
    high_hit_lvl = 50
    ball_highs = [high_lvl_1, high_lvl_2, high_lvl_3, high_lvl_4, high_lvl_5, high_lvl_6, high_lvl_7, high_lvl_8]
    
    #####player var const values
    player_stable = "stable"
    player_moving_right = "right"
    player_moving_left = "left"
    
    #####player vars
    player_move = player_stable
    player2_x = 0
    player2_y = 0
    player2_move = player_stable
    player2_updated = False

    def __init__(self, gamedisp, win_height, win_width):
        self.gameDisplay = gamedisp
        self.window_height = win_height
        self.window_width = win_width
        
        self.window_border_left  = 0
        self.window_border_right = self.window_width

        self.window_border_up = 0
        self.window_border_down = self.window_height - 50#fixme
    
    def balls(self, x, y, color, ball_lvl):
        index = ball_lvl - 1
        if('red' == color):
            self.gameDisplay.blit(pygame.transform.scale(self.ballImg_red, (self.ball_sizes[index], self.ball_sizes[index])), (x,y-self.ball_sizes[index]))
        elif('orange' == color):
            self.gameDisplay.blit(pygame.transform.scale(self.ballImg_orange, (self.ball_sizes[index], self.ball_sizes[index])), (x,y-self.ball_sizes[index]))
        elif('yellow' == color):
            self.gameDisplay.blit(pygame.transform.scale(self.ballImg_yellow, (self.ball_sizes[index], self.ball_sizes[index])), (x,y-self.ball_sizes[index]))
        elif('green' == color):
            self.gameDisplay.blit(pygame.transform.scale(self.ballImg_green, (self.ball_sizes[index], self.ball_sizes[index])), (x,y-self.ball_sizes[index]))
        
    #def remove_balls():
        #fixme ey
    
    def add_ball(self, x, y, color, ball_level, direction, ball_step):
        ball_high = self.window_border_down - y

        ball_node = []
        ball_node.insert(0, x)
        ball_node.insert(1, y)
        ball_node.insert(2, color)
        ball_node.insert(3, ball_level)
        ball_node.insert(4, direction)
        ball_node.insert(5, ball_high)
        ball_node.insert(6, ball_step)#sinüsün neresinde olduğunu gösterir
        #fixme mutex
        self.ball_array.append(ball_node)
    
    def draw_all_balls(self):
        if self.ball_array:
            for ball_node in self.ball_array:
                self.balls(ball_node[0], ball_node[1], ball_node[2], ball_node[3])

    def move_balls(self):
        if self.ball_array:
            for ball_node in self.ball_array:
                #update x
                ballx = ball_node[0]
                ball_direction = ball_node[4]
                if ('right' == ball_direction):
                    ballx = ballx + self.ball_speed_pixels
                    if ballx > self.window_border_right:
                        dif = ballx - self.window_border_right
                        ballx = self.window_border_right - dif
                        ball_node[4] = 'left'
                    ball_node[0] = ballx
                else:
                    ballx = ballx - self.ball_speed_pixels
                    if ballx < self.window_border_left:
                        dif = self.window_border_left - ballx
                        ballx = self.window_border_left + dif
                        ball_node[4] = 'right'
                    ball_node[0] = ballx
                #update y
                index = ball_node[3] - 1 #ball_lvl
                bally = ball_node[1]
                ball_step = ball_node[6]
                ball_high = ball_node[5]
                ball_step = ball_step + 1
                if ball_step > self.pi_steps:
                    ball_step = 0
                    ball_high = self.ball_highs[index]
                high_val = ball_high * math.sin(ball_step * self.one_step_size)
                bally = self.window_border_down - high_val
                ball_node[1] = bally
                ball_node[5] = ball_high
                ball_node[6] = ball_step
          
          
    def check_ball_crash(self, playerx, playery, ball_size, centerx, centery):
        r = ball_size / 2
        if (centery + r) < playery:
            return False
        if (centerx + r) < playerx:
            return False
        if (centerx - r) > (playerx + self.player_image_width):
            return False
        if centery < playery:
            locy = playery - centery
            x_range = (r * r) - (locy * locy)
            if x_range < 0:
                #buraya girmemesi lazım
                return False
            x_range = math.sqrt(x_range)
        else:
            x_range = r
        if (centerx + x_range) < (playerx + self.player_image_width) and (centerx + x_range) > playerx:
            print("ilk yer: playerx: "+str(playerx)+"  playery: "+str(playery)+"  centerx: "+str(centerx)+"  centery: "+str(centery)+"  x_range:"+str(x_range))#FIXME 
            return True
        if (centerx - x_range) < (playerx + self.player_image_width) and (centerx - x_range) > playerx:
            print("ikinci yer: playerx: "+str(playerx)+"  playery: "+str(playery)+"  centerx: "+str(centerx)+"  centery: "+str(centery)+"  x_range:"+str(x_range))#FIXME 
            return True
    
    def check_if_player_crash(self, playerx, playery):
        if self.ball_array:
            for ball_node in self.ball_array:
                ballx = ball_node[0]
                bally = ball_node[1]
                index = ball_node[3] - 1 #ball_lvl
                size = self.ball_sizes[index]
                # Ball location
                centerx = ballx + size / 2
                centery = bally + size / 2
                #player location
                if self.check_ball_crash(playerx, playery, size, centerx, centery):
                    return True
        #Hiçbir top çarpmamış
        return False
            
    def player_crashed(self):
        print("crashed")
        #FIXME ey:
    
    def player_hit_the_ball(self, ball_node):
        self.ball_array.remove(ball_node)
        ball_lvl = ball_node[3]
        if (ball_lvl > 1):
            ball1 = []
            ball2 = []
            
            ball_lvl = ball_lvl - 1
            ballx = ball_node[0]
            bally = ball_node[1] - self.hit_jump_pixels
            color = ball_node[2]
            self.add_ball(ballx, bally, color, ball_lvl, 'right', self.top_step)
            self.add_ball(ballx, bally, color, ball_lvl, 'left', self.top_step)
    
    def check_if_player_hit_ball(self, hookx, hooky):
        if self.ball_array:
            for ball_node in self.ball_array:
                ballx = ball_node[0]
                bally = ball_node[1]
                index = ball_node[3] - 1 #ball_lvl
                size = self.ball_sizes[index]
                # Ball location
                centerx = ballx + size / 2
                centery = bally + size / 2
                r = size / 2
                if centery < hooky:
                    locy = hooky - centery
                    x_range = (r * r) - (locy* locy)
                    if x_range < 0:
                        x_range = 0
                    x_range = math.sqrt(x_range)
                else:
                    x_range = r
                if x_range > 0 and hookx > (centerx - r) and hookx < (centery + r):
                    self.player_hit_the_ball(ball_node)
                    return True
        return False

    def arrow(self, x, y, arrow_size):
        self.gameDisplay.blit(pygame.transform.scale(self.arrowImg, (5, arrow_size)), (x,(y-arrow_size)))
           
    def player_1(self, x, y):
        self.gameDisplay.blit(self.playerImg_1,(x,y-self.player_image_height))
        
    def player_2(self, x, y):
        self.gameDisplay.blit(self.playerImg_2,(x,y-self.player_image_height))
    
    def calculate_and_change_x(self, x, x_change):
        x += x_change
        if x < self.window_border_left:
            x = self.window_border_left
        if x > self.window_border_right:
            x = self.window_border_right
            
        return x
    
    def update_player_2_info(self, x, y, movement):
        self.player2_x = x
        self.player2_y = y
        self.player2_move = movement
        self.player2_updated = True
        
    def move_player_2(self):
        if not self.player2_updated:
            if self.player2_move == self.player_moving_right:
                x_change = self.player_speed_pixels
            elif self.player2_move == self.player_moving_left:
                x_change = -self.player_speed_pixels
            else:
                x_change = 0
            self.player2_x = self.calculate_and_change_x(self.player2_x, x_change)
        else:
            #Bu frame içerisinde zaten veri update edilmiş harekete gerek yok
            self.player2_updated = False
            #Diğer framede veri güncellenmezse hareket ettirilecek
    
    def game_loop(self):
        x = (self.window_width * 0.45)
        y = (self.window_height)
        
        x_change = 0
        
        is_hooking = False
        hook_size = 0
        hook_y = y
        hook_x = x #will be overriden, does not really matter
        
        gameExit = False
     
        self.add_ball(650, 100, 'red', 8, 'right', self.top_step) #fixme ey: gidici
        
        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
     
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -self.player_speed_pixels
                        self.player_move = self.player_moving_left
                    if event.key == pygame.K_RIGHT:
                        x_change = self.player_speed_pixels
                        self.player_move = self.player_moving_right
                    if event.key == pygame.K_UP:
                        if not is_hooking:
                            is_hooking = True
                            hook_size = self.hook_speed_pixels
                            hook_x = x
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0
                        self.player_move = self.player_stable
            
            if is_hooking:
                hook_size += self.hook_speed_pixels
                if (hook_y - hook_size) <= 0:
                    is_hooking = False
            
            self.move_balls()
            x = self.calculate_and_change_x(x, x_change)

            is_crashed = self.check_if_player_crash(x, y)
            if is_crashed:
                self.player_crashed()
            
            self.move_player_2()
            
            self.gameDisplay.fill(self.white)
            
            self.player_1(x, y)
            self.player_2(self.player2_x, self.player2_y)
            if is_hooking:
                self.arrow(hook_x, hook_y, hook_size)
                can_hit = self.check_if_player_hit_ball(hook_x, hook_y - hook_size)
                if can_hit:
                    is_hooking = False
            self.draw_all_balls()
        
            pygame.display.update()
            self.clock.tick(60)


