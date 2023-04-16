import random
import time
import pygame
from pygame.locals import *

pygame.init()

# Constants
WIDTH = 900
HEIGHT = 600
PLAYER_SPEED = 51
player_start_x = 17
player_start_y = 35
bot1_x = 425
bot1_y = 137
bot2_x = 119
bot2_y = 443
bot3_x = 527
bot3_y = 443

# game space
LEFT = 17
RIGHT = 833
UP = 35
DOWN = 545

# Basic color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load images
menu_background = pygame.image.load("menu_background.jpg")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
soundtrack = pygame.mixer.music.load("soundtrack.mp3")
pygame.mixer.music.play(-1)
bomb_sound = pygame.mixer.Sound("bomb.mp3")
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (45, 50))
bomb_image = pygame.image.load("bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (45, 45))
wall_image = pygame.image.load("wall.png")
wall_image = pygame.transform.scale(wall_image, (50, 50))
explosion_image = pygame.image.load("explosion.png")
explosion_image = pygame.transform.scale(explosion_image, (51, 51))
bot1_image = pygame.image.load("bot1.png")
bot1_image = pygame.transform.scale(bot1_image, (50, 50))
bot2_image = pygame.image.load("bot2.png")
bot2_image = pygame.transform.scale(bot2_image, (50, 50))
bot3_image = pygame.image.load("bot3.png")
bot3_image = pygame.transform.scale(bot3_image, (50, 50))

# Initialize font
font_small = pygame.font.SysFont('sans', 10)

# list of coordinates of the walls
wall_list =  [(17, 188), (17, 392), 
            (68, 239), (68, 443), 
            (119, 86), (119, 188), (119, 290), (119, 392), (119, 494), 
            (170, 35), (170, 137), (170, 341), (170, 545), 
            (221, 86), (221, 290), (221, 494), 
            (272, 137), (272, 239), (272, 341), 
            (323, 188), (323, 290), (323, 392), (323, 494), 
            (374, 137), (374, 341), (374, 443), (374, 545), 
            (425, 86), (425, 188), (425, 392), 
            (476, 35), (476, 239), (476, 341), 
            (527, 188), (527, 494), 
            (578, 35), (578, 341), (578, 443), (578, 545), 
            (629, 86), (629, 188), (629, 290), (629, 392), 
            (680, 137), (680, 239), (680, 443), 
            (731, 86), (731, 188), (731, 392), (731, 494), 
            (782, 35), (782, 137), (782, 239), (782, 341), (782, 545), 
            (833, 188), (833, 392)]

# list of cells that cannot be entered
blocked_coordinates = [(17, 188), (17, 392), 
                    (68, 239), (68, 443), 
                    (119, 86), (119, 188), (119, 290), (119, 392), (119, 494), 
                    (170, 35), (170, 137), (170, 341), (170, 545), 
                    (221, 86), (221, 290), (221, 494), 
                    (272, 137), (272, 239), (272, 341), 
                    (323, 188), (323, 290), (323, 392), (323, 494), 
                    (374, 137), (374, 341), (374, 443), (374, 545), 
                    (425, 86), (425, 188), (425, 392), 
                    (476, 35), (476, 239), (476, 341), 
                    (527, 188), (527, 494), 
                    (578, 35), (578, 341), (578, 443), (578, 545), 
                    (629, 86), (629, 188), (629, 290), (629, 392), 
                    (680, 137), (680, 239), (680, 443), 
                    (731, 86), (731, 188), (731, 392), (731, 494), 
                    (782, 35), (782, 137), (782, 239), (782, 341), (782, 545), 
                    (833, 188), (833, 392)]

all_row_and_cloumn = []
# get all coordinates of columns
for col in range(17,834, 51):
    for row in range(35,545 ,51):
        if col % 2 == 0 and row % 2 == 0:
            all_row_and_cloumn.append((col, row))


# Define Player class
class Player:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    # move up 1 cell
    def move_up(self):
        if (self.x, self.y - PLAYER_SPEED) not in blocked_coordinates and self.y > UP and (self.x - 17) / PLAYER_SPEED % 2 == 0:
            self.y -= PLAYER_SPEED

    # move down 1 cell
    def move_down(self):
        if (self.x, self.y + PLAYER_SPEED) not in blocked_coordinates and self.y < DOWN and (self.x - 17) / PLAYER_SPEED % 2 == 0:
            self.y += PLAYER_SPEED

    # move left 1 cell
    def move_left(self):
        if (self.x - PLAYER_SPEED, self.y) not in blocked_coordinates and self.x > LEFT and (self.y - 35) / PLAYER_SPEED % 2 == 0:
            self.x -= PLAYER_SPEED

    # move right 1 cell
    def move_right(self):
        if (self.x + PLAYER_SPEED, self.y) not in blocked_coordinates and self.x < RIGHT and (self.y - 35) / PLAYER_SPEED % 2 == 0:
            self.x += PLAYER_SPEED

    # draw palyer on screen
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# define bot class
class Bot:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.movement_speed = 51
        self.time_to_move = 300
        self.last_move_time = pygame.time.get_ticks()

    # draw bot on screen
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    # Initialize random direction for bot
    def update(self):
        # Check if it's time to move
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.time_to_move:
            # Time to move, generate a random number to decide to move left or right
            direction = random.choice(['left', 'right', 'up', 'down'])
            if direction == 'left'and self.x - self.movement_speed >= LEFT and (self.x - self.movement_speed, self.y) not in blocked_coordinates and (self.x - self.movement_speed, self.y) not in all_row_and_cloumn:
                self.x -= self.movement_speed
            elif direction == 'right' and self.x + self.movement_speed <= RIGHT and (self.x + self.movement_speed, self.y) not in blocked_coordinates and (self.x + self.movement_speed, self.y) not in all_row_and_cloumn:
                self.x += self.movement_speed
            elif direction == 'up' and self.y - self.movement_speed >= UP and (self.x, self.y - self.movement_speed) not in blocked_coordinates and (self.x, self.y - self.movement_speed) not in all_row_and_cloumn:
                self.y -= self.movement_speed
            elif direction == 'down' and self.y + self.movement_speed <= DOWN and (self.x, self.y + self.movement_speed) not in blocked_coordinates and (self.x, self.y + self.movement_speed) not in all_row_and_cloumn:
                self.y += self.movement_speed
            # Update bot travel time
            self.last_move_time = current_time

wall_will_remove = []

# define bomb class
class Bomb:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.explode_time = pygame.time.get_ticks() + 1700  # set 1,7 seconds timer
        self.exploded = False
        self.neighbor_explosions = []
        
    # clear the wall if hit by an explosion
    def delete_wall(self ,test_x, test_y):
        if (test_x, test_y) in blocked_coordinates:
            blocked_coordinates.remove((test_x, test_y))
            wall_will_remove.append((test_x,test_y))
            pygame.display.update()

    # check explosive zones and explosive cells
    def calculate_neighbor_explosions(self):
        neighbors = []
        
        if (self.x + PLAYER_SPEED, self. y) in all_row_and_cloumn or (self.x - PLAYER_SPEED, self.y) in all_row_and_cloumn:
            neighbors.append((self.x, self.y + PLAYER_SPEED))
            neighbors.append((self.x, self.y - PLAYER_SPEED))

            if (self.x, self.y + PLAYER_SPEED) not in blocked_coordinates:
                neighbors.append((self.x, self.y + PLAYER_SPEED * 2))
                self.delete_wall(self.x, self.y + PLAYER_SPEED * 2)

            if (self.x, self.y - PLAYER_SPEED * 2) not in blocked_coordinates:
                neighbors.append((self.x, self.y - PLAYER_SPEED * 2))
                self.delete_wall(self.x, self.y - PLAYER_SPEED * 2)

            self.delete_wall(self.x, self.y + PLAYER_SPEED)
            self.delete_wall(self.x, self.y - PLAYER_SPEED)

        if ((self.x + PLAYER_SPEED, self.y) not in all_row_and_cloumn or (self.x - PLAYER_SPEED, self.y) not in all_row_and_cloumn) and ((self.x, self.y + PLAYER_SPEED) not in all_row_and_cloumn or (self.x, self.y - PLAYER_SPEED) not in all_row_and_cloumn):
            neighbors.append((self.x + PLAYER_SPEED, self.y))
            neighbors.append((self.x - PLAYER_SPEED, self.y))
            neighbors.append((self.x, self.y + PLAYER_SPEED))
            neighbors.append((self.x, self.y - PLAYER_SPEED))

            if (self.x + PLAYER_SPEED, self.y) not in blocked_coordinates:
                neighbors.append((self.x + PLAYER_SPEED * 2, self.y))
                self.delete_wall(self.x + PLAYER_SPEED * 2, self.y)
            if (self.x - PLAYER_SPEED, self.y) not in blocked_coordinates:
                neighbors.append((self.x - PLAYER_SPEED * 2, self.y))
                self.delete_wall(self.x - PLAYER_SPEED * 2, self.y)

            if (self.x, self.y + PLAYER_SPEED) not in blocked_coordinates:
                neighbors.append((self.x, self.y + PLAYER_SPEED * 2))
                self.delete_wall(self.x, self.y + PLAYER_SPEED * 2)
            if (self.x, self.y - PLAYER_SPEED) not in blocked_coordinates:
                neighbors.append((self.x, self.y - PLAYER_SPEED * 2))
                self.delete_wall(self.x, self.y - PLAYER_SPEED * 2)

            self.delete_wall(self.x + PLAYER_SPEED, self.y)
            self.delete_wall(self.x - PLAYER_SPEED, self.y)
            self.delete_wall(self.x, self.y + PLAYER_SPEED)
            self.delete_wall(self.x, self.y - PLAYER_SPEED)

        if ((self.x + PLAYER_SPEED, self.y) not in all_row_and_cloumn or (self.x - PLAYER_SPEED, self.y) not in all_row_and_cloumn) and ((self.x, self.y + PLAYER_SPEED) in all_row_and_cloumn or (self.x, self.y - PLAYER_SPEED) in all_row_and_cloumn):
            neighbors.append((self.x + PLAYER_SPEED, self.y))
            neighbors.append((self.x - PLAYER_SPEED, self.y))


            if (self.x + PLAYER_SPEED, self.y) not in blocked_coordinates:
                neighbors.append((self.x + PLAYER_SPEED * 2, self.y))
                self.delete_wall(self.x + PLAYER_SPEED * 2, self.y)
            if (self.x - PLAYER_SPEED, self.y) not in blocked_coordinates:
                neighbors.append((self.x - PLAYER_SPEED * 2, self.y))
                self.delete_wall(self.x - PLAYER_SPEED * 2, self)

            self.delete_wall(self.x + PLAYER_SPEED, self.y)
            self.delete_wall(self.x - PLAYER_SPEED, self.y)

        for neighbor in neighbors:
            x, y = neighbor
            
            if self.x == x and LEFT <= x <= RIGHT and UP <= y <= DOWN and (self.y - 35) / PLAYER_SPEED % 2 == 1:
                self.neighbor_explosions.append((x, y))

            if self.y == y and LEFT <= x <= RIGHT and UP <= y <= DOWN and (self.x - 17) / PLAYER_SPEED % 2 == 1:
                self.neighbor_explosions.append((x, y))

            if LEFT <= x <= RIGHT and UP <= y <= DOWN and (self.x - 17) / PLAYER_SPEED % 2 == 0 and (self.y - 35) / PLAYER_SPEED % 2 == 0:
                self.neighbor_explosions.append((x, y))

            if LEFT <= x <= RIGHT and UP <= y <= DOWN and (self.y - 35) / PLAYER_SPEED % 2 == 0 and (self.x - 17) / PLAYER_SPEED % 2 == 0:
                self.neighbor_explosions.append((x, y))
                
    def draw(self, screen):
        if not self.exploded:
            screen.blit(self.image, (self.x, self.y))
            if pygame.time.get_ticks() > self.explode_time:  # explode bomb after 2 seconds
                self.image = explosion_image
                self.explode_time = pygame.time.get_ticks() + 300  # set 300ms timer for flame
                self.exploded = True
                self.calculate_neighbor_explosions()

        else:
            if pygame.time.get_ticks() > self.explode_time:  # remove flame after 300ms
                self.image = None
            else:
                for exploosion_pos in self.neighbor_explosions:
                    screen.blit(self.image, exploosion_pos)

        if self.image:
            screen.blit(self.image, (self.x, self.y))
        
# define wall class
class Wall:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    # function to draw wall on screen
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# define Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    # function to draw button on screen
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        font = pygame.font.SysFont('sans', 20)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

# initialize the start button
start_button = Button(350, 250, 200, 50, "Start Game")

# initialize the quit button
quit_button = Button(350, 325, 200, 50, "Quit Game")

# initialize the win button
win_button = Button(350, 300, 200, 50, "WIN")

# initialize the lose button
lose_button = Button(350, 300, 200, 50, "LOSE")

# Initialize player object
player = Player(player_start_x, player_start_y, player_image)

# initialize bot objects
bot1 = Bot(bot1_x, bot1_y, bot1_image)
bot2 = Bot(bot2_x, bot2_y, bot2_image)
bot3 = Bot(bot3_x, bot3_y, bot3_image)

# get the coordinates of the bots
bot1_pos = (bot1.x, bot1.y)
bot2_pos = (bot2.x, bot2.y)
bot3_pos = (bot3.x, bot3.y)

# Initialize bomb object
bomb = None

# Initialize the explosion object
explosion = None

# Initialize wall objects
wall_objects = []
for wall_pos in wall_list:
    wall = Wall(wall_pos[0], wall_pos[1], wall_image)
    wall_objects.append(wall)

for wall in wall_will_remove:
    wall_objects.remove(wall)

# Initialize screen
pygame.display.set_caption("Bomberman")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# display menu on screen
menu = True
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.rect.collidepoint(event.pos):
                menu = False
                running = True
            elif quit_button.rect.collidepoint(event.pos):
                menu = False
                running = False
    
    screen.blit(menu_background, (0, 0))
    start_button.draw(screen)
    quit_button.draw(screen)

    pygame.display.flip()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check moves and place bombs
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move_up()
            elif event.key == pygame.K_DOWN:
                player.move_down()
            elif event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()

            # create bomb when space key is pressed
            elif event.key == pygame.K_SPACE and not bomb:  
                bomb = Bomb(player.x, player.y, bomb_image)
                bomb_sound.play()
                
    # Draw images and text
    screen.blit(background_image, (0, 0))

    # Draw wall objects
    for wall in wall_objects :
        if (wall.x, wall.y) not in wall_will_remove:
            wall.draw(screen)
    
    # if the player places a bomb
    if bomb:
        bomb.draw(screen)
        # explode bomb after 2 seconds
        if pygame.time.get_ticks() > bomb.explode_time:  

            pos = bot1.x, bot1.y
            # set the bot's coordinates outside the screen
            if pos in bomb.neighbor_explosions or pos == (bomb.x,bomb.y):
                bot1.x = -10000  
                bot1.y = -10000
                bot1.update()

            pos2 = bot2.x, bot2.y
            # set the bot's coordinates outside the screen
            if pos2 in bomb.neighbor_explosions or pos2 == (bomb.x,bomb.y):
                bot2.x = -10000  
                bot2.y = -10000
                bot2.update()
                
            pos3 = bot3.x, bot3.y
            # set the bot's coordinates outside the screen
            if pos3 in bomb.neighbor_explosions or pos3 == (bomb.x,bomb.y):
                bot3.x = -10000  
                bot3.y = -10000
                bot3.update()

            pos_player = player.x, player.y
            # If the player is in the explosion zone, it won't show up on the screen
            if  pos_player in bomb.neighbor_explosions or pos_player == (bomb.x, bomb.y):
                player.x = -10000
                player.y = -10000   
            
            bomb = None

    win = False
    lose = False

    # check for collision between player and bot
    if (player.x, player.y) in [(bot1.x, bot1.y), (bot2.x, bot2.y), (bot3.x, bot3.y)]:
        lose = True

    # check if the player has been hit by an explosive bomb
    if player.x < 0 and player.y < 0:
        lose = True

    # check if all bots are hit by bombs
    if (bot1.x < 0) and (bot2.x < 0) and (bot3.x < 0):
        win = True
    
    # loser screen
    while lose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lose = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if lose_button.rect.collidepoint(event.pos):
                    lose = False
                    running = False
        
        screen.blit(menu_background, (0, 0))
        lose_button.draw(screen)

        pygame.display.flip()

    # victory screen
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if win_button.rect.collidepoint(event.pos):
                    win = False
                    running = False
        
        screen.blit(menu_background, (0, 0))
        win_button.draw(screen)

        pygame.display.flip()

    # update bot posion
    bot1.update()
    bot2.update()
    bot3.update()

    # draw objects
    player.draw(screen)
    bot1.draw(screen)
    bot2.draw(screen)
    bot3.draw(screen)

    # print the cursor coordinates to the screen
    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # text_mouse = font_small.render("(" + str(mouse_x) + "," + str(mouse_y) + ")", True, BLACK)
    # screen.blit(text_mouse, (mouse_x + 10, mouse_y))

    # print "player" on top player
    text_player = font_small.render("Player", True, BLACK)
    screen.blit(text_player, (player.x + 10, player.y - 10))

    # print "black panther" on top bot 1
    text_bot1 = font_small.render("Black panter", True, BLACK)
    screen.blit(text_bot1, (bot1.x + 6, bot1.y - 10))

    # print "Spiderman" on top bot 2
    text_bot2 = font_small.render("Spiderman", True, BLACK)
    screen.blit(text_bot2, (bot2.x + 6, bot2.y - 10))

    # print "Ironman" on top bot 3
    text_bot3 = font_small.render("Ironman", True, BLACK)
    screen.blit(text_bot3, (bot3.x + 6, bot3.y - 10))

    # Update screen
    pygame.display.flip()

# Quit game
pygame.quit()