import pygame
import pathlib
import hex
import os

try:
    os.environ["DISPLAY"]
except:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

os.environ['SDL_AUDIODRIVER'] = 'dsp'


pygame.init()

screen = pygame.display.set_mode([500, 500])
image = pygame.image.load(
        os.path.join(
        os.path.dirname(__file__),
        "../images/boat.png"
        )
    ).convert_alpha()
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
