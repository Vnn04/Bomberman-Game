import pygame
from pygame.locals import *
from pynput import keyboard
import time

pygame.init()

screen = pygame.display.set_mode((911, 911))

pygame.display.set_caption('My Game')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

running = True

#x, y cua người chơi
bot = [0, 0]

while running:
    screen.fill(BLACK)

    #draw grid
    for i in range(26):
        pygame.draw.line(screen, WHITE, (0, 70 * i), (910, 70 * i))
        pygame.draw.line(screen, WHITE, (i * 70, 0), (i * 70, 910))
    
    #draw human
    pygame.draw.rect(screen, GREEN, (bot[0] * 35, bot[1] * 35, 70, 70))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
        
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP):
                if bot[1] > 0:
                    bot[1] = bot[1] - 1
                    print("up")
            elif (event.key == pygame.K_DOWN):
                if bot[1] < 24:
                    bot[1] = bot[1] + 1
                    print("down")

            elif (event.key == pygame.K_LEFT):
                if bot[0] > 0:
                    bot[0] = bot[0] - 1
                    print("left")

            elif (event.key == pygame.K_RIGHT):
                if bot[0] < 24:
                    bot[0] = bot[0] + 1 
                    print("right")


    pygame.display.flip()


pygame.quit()