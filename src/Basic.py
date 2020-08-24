import pygame
import hex

pygame.init()

screen = pygame.display.set_mode([500, 500])
image = pygame.image.load("boat.png").convert_alpha()
running = True

boat = hex.Hex(100, image, (255,0,0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))

    boat.draw(screen, (0, 0))
    pygame.display.update()

pygame.quit()
