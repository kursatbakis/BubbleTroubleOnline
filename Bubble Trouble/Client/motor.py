import pygame
import time
import json
import random
import math
from clientNetwork import coordinatesPacket, deadPacket, hitBallPacket, send_udp_packet, udpSocket
from window import getPlayerID

class BubbleGameConstants:
    #####player var const values
    player_stable = "stable"
    player_moving_right = "right"
    player_moving_left = "left"
    
    player_image_height = 37
    player_image_width = 23
    
    #speeds
    player_speed_pixels = 5
    hook_speed_pixels = 15
    ball_speed_pixels = 3
    
    hit_jump_pixels = 50
    
    #####protection
    player_protection_frames = 100
    player_blink_frames = 10
    
    #####life
    player_start_life = 5
    
    #####update rate
    player_update_per_frames = 5

class BubblePlayer:
    #player_x
    #player_y 
    #window_border_left
    #window_border_right
    player_move = BubbleGameConstants.player_stable
    
    #gameDisplay
    
    player_updated = False
    
    
    player_shield_active = True
    player_protection = BubbleGameConstants.player_protection_frames
    player_shield_blink = BubbleGameConstants.player_blink_frames
    player_visible = True
    
    is_shooting = False
    arrow_size = 0
    #arrow_y
    arrow_x = 0 #will be overriden, does not really matter
    #arrowImg
    
    player_score = 0
    player_lifes = BubbleGameConstants.player_start_life
    
    def __init__(self, gamescreen, x, y, img, border_left, border_right, arw_img, player_id):
        self.gameDisplay = gamescreen
        self.player_x = x
        self.player_y = y
        self.player_img = img
        self.window_border_left = border_left
        self.window_border_right = border_right
        self.arrow_y = y
        self.arrowImg = arw_img
        self.playerID = player_id
        
    def activate_player_shield(self):
        self.player_shield_active = True
        self.player_protection = BubbleGameConstants.player_protection_frames
        self.player_shield_blink = BubbleGameConstants.player_blink_frames
        self.player_visible = True
    
    def iterate_shield_params(self):
        self.player_protection = self.player_protection - 1
        if self.player_protection <= 0:
            self.player_shield_active = False
            self.player_visible = True
        else:
            self.player_shield_blink = self.player_shield_blink - 1
            if self.player_shield_blink <= 0:
                self.player_shield_blink = BubbleGameConstants.player_blink_frames
                if self.player_visible:
                    self.player_visible = False
                else:
                    self.player_visible = True
        
    def prepare_shooting_msg():
        if self.is_shooting:
            pack = {'arr_size': self.arrow_size, 'arrx': self.arrow_x, 'arry': self.arrow_y}
            return json.dumps(pack)
        else:
            return None
    
    def prepare_shield_msg():
        if self.player_shield_active:
            pack = {'prot_time': self.player_protection, 'blink_time': self.player_shield_blink, 'visible': self.player_visible}
            return json.dumps(pack)
        else:
            return None
    
    def send_player_coordinates():
        shooting_msg = self.prepare_shooting_msg()
        shield_msg = self.prepare_shield_msg()
        msg = coordinatesPacket(self.playerID, -1, self.player_x, self.player_move, shooting_msg, shield_msg)
        send_udp_packet(msg, udpSocket())
        
    def player_crashed(self):
        if not self.player_shield_active:
            self.player_lifes = self.player_lifes - 1
            self.activate_player_shield()
            print("crashed, life remain: "+str(self.player_lifes))
            
            msg = deadPacket(self.playerID, self.player_lifes)
            send_udp_packet(msg, udpSocket())
    
    def iterate_arrow(self):
        self.arrow_size += BubbleGameConstants.hook_speed_pixels
        if (self.arrow_y - self.arrow_size) <= 0:
            self.is_shooting = False
        
    def draw_arrow(self, x, y, arrow_size):
        self.gameDisplay.blit(pygame.transform.scale(self.arrowImg, (5, arrow_size)), (x,(y-arrow_size)))
        
    def draw_player(self):
        if self.player_shield_active:
            self.iterate_shield_params()
        if self.player_visible:
            self.gameDisplay.blit(self.player_img,(self.player_x,self.player_y-BubbleGameConstants.player_image_height))
        if self.is_shooting:
            self.iterate_arrow()
            self.draw_arrow(self.arrow_x, self.arrow_y, self.arrow_size)
    
    def update_player_info(self, x, movement, shooting_msg, shield_msg):
        self.player_x = x
        self.player_move = movement
        if shooting_msg:
            self.is_shooting = True
            content = json.loads(shooting_msg)
            self.arrow_size = content['arr_size']
            self.arrow_x = content['arrx']
            self.arrow_y = content['arry']
        if shield_msg:
            self.player_shield_active = True
            content = json.loads(shield_msg)
            self.player_protection = content['prot_time']
            self.player_shield_blink = content['blink_time']
            self.player_visible = content['visible']
        self.player_updated = True
        
    def calculate_and_change_x(self, x, x_change):
        x += x_change
        if x < self.window_border_left:
            x = self.window_border_left
        if x > self.window_border_right:
            x = self.window_border_right
            
        return x
        
    def move_player_auto(self):
        if not self.player_updated:
            if self.player_move == BubbleGameConstants.player_moving_right:
                x_change = BubbleGameConstants.player_speed_pixels
            elif self.player_move == BubbleGameConstants.player_moving_left:
                x_change = -BubbleGameConstants.player_speed_pixels
            else:
                x_change = 0
            self.player_x = self.calculate_and_change_x(self.player_x, x_change)
        else:
            #Bu frame içerisinde zaten veri update edilmiş harekete gerek yok
            self.player_updated = False
            #Diğer framede veri güncellenmezse hareket ettirilecek
    
    def shoot(self, x):
        self.is_shooting = True
        self.arrow_size = BubbleGameConstants.hook_speed_pixels
        self.arrow_x = x
    
    def arrow_hit(self):
        self.is_shooting = False
        self.player_score = self.player_score + 1

class BubbleGame:
    ######window
    #window_height = 600
    #window_width = 800
    #window_border_left
    #window_border_right
    #window_border_up
    #window_border_down

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

    ball_colors = {'red', 'orange', 'yellow', 'green'}
    
    playerImg_1 = pygame.transform.scale(pygame.image.load('Images/player.png'), (BubbleGameConstants.player_image_width, BubbleGameConstants.player_image_height))
    playerImg_2 = pygame.transform.scale(pygame.image.load('Images/player2.png'), (BubbleGameConstants.player_image_width, BubbleGameConstants.player_image_height))

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
    
    #####Players
    player_self = None
    player_other = None
    
    self.playerID = -1
    send_coordinates = BubbleGameConstants.player_update_per_frames
    
    game_initted = False
    
    def __init__(self, gamedisp, win_height, win_width):
        self.gameDisplay = gamedisp
        self.window_height = win_height
        self.window_width = win_width
        
        self.window_border_left  = 0
        self.window_border_right = self.window_width

        self.window_border_up = 0
        self.window_border_down = self.window_height
    
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
        
    def add_ball(self, x, y, color, ball_level, direction, ball_step, ball_id):
        ball_high = self.window_border_down - y

        ball_node = []
        ball_node.insert(0, x)
        ball_node.insert(1, y)
        ball_node.insert(2, color)
        ball_node.insert(3, ball_level)
        ball_node.insert(4, direction)
        ball_node.insert(5, ball_high)
        ball_node.insert(6, ball_step)#sinüsün neresinde olduğunu gösterir
        ball_node.insert(7, ball_id)
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
                    ballx = ballx + BubbleGameConstants.ball_speed_pixels
                    if ballx > self.window_border_right:
                        dif = ballx - self.window_border_right
                        ballx = self.window_border_right - dif
                        ball_node[4] = 'left'
                    ball_node[0] = ballx
                else:
                    ballx = ballx - BubbleGameConstants.ball_speed_pixels
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
        if (centery + r) < (playery-BubbleGameConstants.player_image_height):
            return False
        if (centerx + r) < playerx:
            return False
        if (centerx - r) > (playerx + BubbleGameConstants.player_image_width):
            return False
        if centery < (playery-BubbleGameConstants.player_image_height):
            locy = (playery-BubbleGameConstants.player_image_height) - centery
            x_range = (r * r) - (locy * locy)
            if x_range < 0:
                #buraya girmemesi lazım
                return False
            x_range = math.sqrt(x_range)
        else:
            x_range = r
        if (centerx + x_range) < (playerx + BubbleGameConstants.player_image_width) and (centerx + x_range) > playerx:
            return True
        if (centerx - x_range) < (playerx + BubbleGameConstants.player_image_width) and (centerx - x_range) > playerx:
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
                centery = bally - size / 2
                #player location
                if self.check_ball_crash(playerx, playery, size, centerx, centery):
                    return True
        #Hiçbir top çarpmamış
        return False
            
    def split_the_ball(self, ball_node, left_id, right_id):
        self.ball_array.remove(ball_node)
        ball_lvl = ball_node[3]
        if (ball_lvl > 1):
            ball1 = []
            ball2 = []
            
            ball_lvl = ball_lvl - 1
            ballx = ball_node[0]
            bally = ball_node[1] - BubbleGameConstants.hit_jump_pixels
            color = ball_node[2]
            self.add_ball(ballx, bally, color, ball_lvl, 'right', self.top_step, right_id)
            self.add_ball(ballx, bally, color, ball_lvl, 'left', self.top_step, left_id)
    
    #FIXME: response func
    def find_and_split_ball(self, removeid, leftid, rightid):
        if self.ball_array:
            for ball_node in self.ball_array:
                if removeid == ball_node[7]:
                    self.split_the_ball(ball_node, leftid, rightid)
    
    def player_hit_the_ball(self, ball_node):
        msg = hitBallPacket(self.playerID, ball_node[7])
        send_udp_packet(msg, udpSocket())
    
    def check_if_player_hit_ball(self, hookx, hooky):
        if self.ball_array:
            for ball_node in self.ball_array:
                ballx = ball_node[0]
                bally = ball_node[1]
                index = ball_node[3] - 1 #ball_lvl
                size = self.ball_sizes[index]
                # Ball location
                centerx = ballx + size / 2
                centery = bally - size / 2
                r = size / 2
                if centery < hooky:
                    locy = hooky - centery
                    x_range = (r * r) - (locy* locy)
                    if x_range < 0:
                        x_range = 0
                    x_range = math.sqrt(x_range)
                else:
                    x_range = r
                if x_range > 0 and hookx > (centerx - r) and hookx < (centerx + r):
                    print("centerx: "+str(centerx)+"  centery: "+str(centery)+"  r: "+str(r)+"  x_range: "+str(x_range)+ "  hookx: "+str(hookx)+"  hooky: "+str(hooky))
                    self.player_hit_the_ball(ball_node)
                    return True
        return False

    def check_and_send_coordinates():
        self.send_coordinates = self.send_coordinates - 1
        if self.send_coordinates <= 0:
            self.player_self.send_player_coordinates()
            self.send_coordinates = BubbleGameConstants.player_update_per_frames   
    
    #FIXME response
    def init_bubble_game(r_lives, balls, x, rivalx, wait):
        y = (self.window_height)
        self.playerID = getPlayerID()
        self.player_self = BubblePlayer(self.gameDisplay, x, y, self.playerImg_1, self.window_border_left, self.window_border_right, self.arrowImg, self.playerID)
        self.player_other = BubblePlayer(self.gameDisplay, rivalx, y, self.playerImg_2, self.window_border_left, self.window_border_right, self.arrowImg, -1)
        if balls:
            for ball_js in balls:
                content = json.loads(shield_msg)
                x = content['x']
                y = content['y']
                ball_level = content['size']
                color_num = content['clr']
                color = self.ball_colors[color_num]
                ball_id = content['ballid']
                direction = content['direction']
                self.add_ball(x, y, color, ball_level, direction, self.top_step, ball_id)
        #FIXME wait:
        self.game_initted = True
           
    #FIXME response
    def update_opponent_info(self, x, movement, shooting_msg, shield_msg):
        self.player_other.update_player_info(self, x, movement, shooting_msg, shield_msg)
    
    def game_loop(self):
        while not self.game_initted:
            time.sleep(0.1) #oyunun init edilmesi bekleniyor
    
        x = (self.window_width * 0.45)
        y = (self.window_height)
        
        x_change = 0
        
        gameExit = False
     
        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
     
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -BubbleGameConstants.player_speed_pixels
                        self.player_self.player_move = BubbleGameConstants.player_moving_left
                    if event.key == pygame.K_RIGHT:
                        x_change = BubbleGameConstants.player_speed_pixels
                        self.player_self.player_move = BubbleGameConstants.player_moving_right
                    if event.key == pygame.K_UP:
                        if not self.player_self.is_shooting:
                            self.player_self.shoot(x)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0
                        self.player_self.player_move = BubbleGameConstants.player_stable
            
            self.move_balls()
            x = self.player_self.calculate_and_change_x(x, x_change)
            self.player_self.player_x = x

            is_crashed = self.check_if_player_crash(self.player_self.player_x, self.player_self.player_y)
            if is_crashed:
                self.player_self.player_crashed()
            
            self.player_other.move_player_auto()
            
            self.gameDisplay.fill(self.white)
            
            self.player_self.draw_player()
            self.player_other.draw_player()
            if self.player_self.is_shooting:
                can_hit = self.check_if_player_hit_ball(self.player_self.arrow_x, self.player_self.arrow_y - self.player_self.arrow_size)
                if can_hit:
                    self.player_self.arrow_hit()
            self.draw_all_balls()
        
            pygame.display.update()
            self.check_and_send_coordinates()
            self.clock.tick(60)


