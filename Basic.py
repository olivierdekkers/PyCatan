import pygame
import hex

pygame.init()

screen = pygame.display.set_mode([500, 500])
image = pygame.image.load("boat.png").convert_alpha()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))

    hex.draw_ngon(screen, (250, 255,255), 6, 100, (100,100), image)
    pygame.display.update()

pygame.quit()
