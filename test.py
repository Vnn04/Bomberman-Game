import pygame
from pygame.locals import *
import random

# define some basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# define game constants
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_VELOCITY = 5
BOMB_RADIUS = 50
BOMB_COUNTDOWN = 3

# initialize Pygame
pygame.init()

# set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bomberman")

# load game assets
background_image = pygame.image.load(r"C:\Users\nguye\Documents\Code Python\background.png").convert()
player_image = pygame.image.load(r"C:\Users\nguye\Documents\Code Python\player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
bomb_image = pygame.image.load(r"C:\Users\nguye\Downloads\bomb.png").convert_alpha()
bomb_image = pygame.transform.scale(bomb_image, (BOMB_RADIUS, BOMB_RADIUS))

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image
        self.velocity = PLAYER_VELOCITY
    
    def move(self, dx, dy):
        self.rect.x += dx * self.velocity
        self.rect.y += dy * self.velocity
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Bomb:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - BOMB_RADIUS//2, y - BOMB_RADIUS//2, BOMB_RADIUS, BOMB_RADIUS)
        self.image = bomb_image
        self.countdown = BOMB_COUNTDOWN
    
    def update(self):
        self.countdown -= 1
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# create game objects
player = Player(SCREEN_WIDTH - PLAYER_WIDTH, PLAYER_HEIGHT)
bombs = []

# game loop
running = True
while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)
            elif event.key == pygame.K_UP:
                player.move(0, -1)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1)
            elif event.key == pygame.K_SPACE:
                bombs.append(Bomb(player.rect.centerx, player.rect.centery))
    
    # update game state
    for bomb in bombs:
        bomb.update()
        if bomb.countdown == 0:
            bombs.remove(bomb)
    
    # draw game objects
    screen.blit(background_image, (0, 0))
    player.draw(screen)
    for bomb in bombs:
        bomb.draw(screen)
    
    # update the screen
    pygame.display.update()

# quit Pygame when the game loop is finished
pygame.quit()