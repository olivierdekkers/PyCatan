import pygame
from math import cos, sin

class Hex:

    def __init__(self, size, image, color):
        self._size = size
        self._image = pygame.transform.scale(image, (2*self._size,2*self._size))
        pi2 = 2 * 3.14159265358979
        self.pointList = [
            (
                cos(i / 6 * pi2 + pi2/4) * self._size + self._size,
                sin(i / 6 * pi2 + pi2/4) * self._size + self._size
            )
            for i in range(0, 6)
        ]
        self.upperLeft = (
            min(self.pointList, key=lambda x: x[0])[0],
            min(self.pointList, key=lambda x: x[1])[1]
        )
        self.pointList = [
            (x-self.upperLeft[0], y-self.upperLeft[1]) for (x,y) in self.pointList
        ]
        self.upperLeft = (0,0)
        self.upperRight = (
            max(self.pointList, key=lambda x: x[0])[0],
            min(self.pointList, key=lambda x: x[1])[1]
        )
        self.bottomLeft = (
            min(self.pointList, key=lambda x: x[0])[0],
            max(self.pointList, key=lambda x: x[1])[1]
        )
        self.bottomRight = (
            max(self.pointList, key=lambda x: x[0])[0],
            max(self.pointList, key=lambda x: x[1])[1]
        )
        self.render(color)

    def draw(self, surface, position):
        surface.blit(self._image, position)
        return surface

    def render(self, color):
        mask = pygame.Surface(self._image.get_rect().size)
        mask.set_colorkey((10,10,10))
        mask.fill((255,255,255,0))

        pygame.draw.polygon(
            mask,
            (10, 10, 10),
            self.pointList,
            )
        pygame.draw.polygon(
            mask,
            color,
            self.pointList,
            2
            )
        self._image.blit(mask, (0,0))
