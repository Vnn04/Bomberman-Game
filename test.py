import pygame
from pygame.locals import *
import os

pygame.init()

# Constants
WIDTH = 900
HEIGHT = 600
PLAYER_SPEED = 51

# game space
LEFT = 45
RIGHT = 800
UP = 60
DOWN = 500

# Basic color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255,0,0)
BLUE = (0,0,255)

# Load images
background_image = pygame.image.load(r"C:\Users\nguye\Documents\Bomberman\Choi\Bomberman\background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
player_image = pygame.image.load(r"C:\Users\nguye\Documents\Bomberman\Choi\Bomberman\player.png")
player_image = pygame.transform.scale(player_image, (45, 50))
bomb_image = pygame.image.load(r"C:\Users\nguye\Documents\Bomberman\Choi\Bomberman\bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (45, 45))
wall_image = pygame.image.load(r"C:\Users\nguye\Documents\Bomberman\wall.png")
wall_image = pygame.transform.scale(wall_image, (50, 50))

# Initialize font
font_small = pygame.font.SysFont('sans', 10)

#wall list
wall_list = [(17, 387), (20, 190), (67, 440), (70, 238), (118, 85), (118, 190), (118, 287), (118, 387), (120, 490), (168, 140), (168, 542), (170, 40), (170, 335), (218, 87), (220, 490), (222, 287), (270, 135), (270, 236), (273, 338), (320, 187), (323, 288), (323, 387), (323, 490), (375, 135), (375, 339), (375, 540), (374, 441), (425, 87), (425, 188), (425, 388), (475, 340), (476, 238), (477, 36), (525, 188), (525, 490), (576, 338), (578, 438), (579, 540), (580, 34), (627, 187), (627, 287), (627, 389), (628, 187), (630, 84), (680, 140), (680, 240), (680, 439), (728, 490), (730, 188), (730, 386), (732, 90), (781, 541), (782, 38), (783, 140), (783, 339), (785, 238), (833, 189), (833, 390)]

# Define Player class
class Player:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def move_up(self):
        if self.y > UP and (self.x - 17) / PLAYER_SPEED % 2 == 0:
            self.y -= PLAYER_SPEED

    def move_down(self):
        if self.y < DOWN and (self.x - 17) / PLAYER_SPEED % 2 == 0:
            self.y += PLAYER_SPEED

    def move_left(self):
        if self.x > LEFT and (self.y - 35) / PLAYER_SPEED % 2 == 0:
            self.x -= PLAYER_SPEED

    def move_right(self) :
        if self.x < RIGHT and (self.y - 35) / PLAYER_SPEED % 2 == 0:
            self.x += PLAYER_SPEED

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# define bomb class
class Bomb:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.explode_time = pygame.time.get_ticks() + 3000  # set 3 seconds timer

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# define wall class
class Wall:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Initialize player object
player = Player(17, 35, player_image)

# Initialize bomb object
bomb = None

# Initialize wall objects
wall_objects = []
for wall_pos in wall_list:
    wall = Wall(wall_pos[0], wall_pos[1], wall_image)
    wall_objects.append(wall)

# Initialize screen
pygame.display.set_caption("Bomberman")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Main loop
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move_up()
            elif event.key == pygame.K_DOWN:
                player.move_down()
            elif event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_SPACE and not bomb:  # create bomb when space key is pressed
                bomb = Bomb(player.x, player.y, bomb_image)


    # Draw images and text
    screen.blit(background_image, (0, 0))
    if bomb:
        bomb.draw(screen)
        if pygame.time.get_ticks() > bomb.explode_time:  # explode bomb after 5 seconds
            bomb = None
    player.draw(screen)
    
    # Draw wall objects
    for wall in wall_objects:
        wall.draw(screen)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    text_mouse = font_small.render("(" + str(mouse_x) + "," + str(mouse_y) + ")", True, BLACK)
    screen.blit(text_mouse, (mouse_x + 10, mouse_y))

    # Update screen
    pygame.display.flip()

# Quit game
pygame.quit()