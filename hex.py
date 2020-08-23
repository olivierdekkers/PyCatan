import pygame
from math import cos, sin



def draw_ngon(Surface, color, n, radius, position, image):
    masked_result = pygame.transform.scale(image, (2*radius,2*radius))
    mask_surface = pygame.Surface((2*radius, 2*radius))
    pi2 = 2 * 3.14159265358979
    pointList = [
        (
            cos(i / n * pi2) * radius + position[0],
            sin(i / n * pi2) * radius + position[0]
        )
        for i in range(0, n)
    ]
    pygame.draw.polygon(
        mask_surface,
        color,
        pointList,
        )
    masked_result.blit(mask_surface, (0, 0), None, pygame.BLEND_RGBA_MULT)

    Surface.blit(masked_result, (0,0))
    return
