import pygame

pygame.init()

width, height = 1000, 600
screen = pygame.display.set_mode((width, height))

# color board
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen.fill(BLACK)

pygame.display.flip()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()