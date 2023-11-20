import pygame
from math import cos, sin, ceil

pi2 = 2 * 3.14159265358979
class Hex:

    def __init__(self, size, image, color):
        self.x = 0
        self.y = 0
        self._size = size
        self._image = pygame.transform.scale(image, (2*self._size,2*self._size))
        self._tile = True
        self.color = color
        self._pointList = [
            (
                int(cos(i / 6 * pi2) * self._size + self._size),
                int(sin(i / 6 * pi2) * self._size + self._size)-int(size/10)
            )
            for i in range(0, 6)
        ]
        for index, point in enumerate(self._pointList):
            x = point[0]
            y = point[1]
            if 2 <x % 5:
                x += 5 - x % 5
            elif 0 < x % 5 and x % 5 < 3:
                x -= x % 5

            if 2 < y % 5:
                y += 5 - y % 5
            elif 0 < y % 5  and y % 5 < 3:
                y -= y % 5
            self._pointList[index] = (x,y)
                
        self.height = max(self._pointList, key= lambda x: x[1])[1] - min(self._pointList, key= lambda x: x[1])[1]


    def draw(self, surface):
        surface.blit(self._image, (self.x, self.y))
        return surface

    def render(self):
        minY = min(self._pointList, key= lambda x: x[1])[1]
        self._pointList = [(x,y-minY) for x,y in self._pointList]
        self.height = abs(max(self._pointList, key= lambda x: x[1])[1]) - abs(min(self._pointList, key= lambda x: x[1])[1])
        self._image = pygame.transform.scale(self._image, (2*self._size,ceil(self.height)))
        self._image.set_colorkey((255,255,255))
        mask = pygame.Surface(self._image.get_rect().size)
        mask.set_colorkey((10,10,10))
        mask.fill((255,255,255,0))
        # draw hole in mask?
        pygame.draw.polygon(
            mask,
            (10, 10, 10),
            self._pointList,
            )
        pygame.draw.polygon(
            mask,
            self.color,
            self._pointList,
            3
            )
        self._image.blit(mask, (0,0))

    def translate(self, x,y):
        self.x += x
        self.y += y
        return self


    @property
    def pointList(self):
        return [(self.x +x, self.y + y) for x,y in self._pointList]

    @property
    def upperLeft(self):
        return (self.pointList[4][0], self.pointList[4][1])

    @property
    def upperRight(self):
        return (self.pointList[5][0], self.pointList[5][1])

    @property
    def bottomLeft(self):
        return (self.pointList[2][0], self.pointList[2][1])

    @property
    def bottomRight(self):
        return (self.pointList[1][0], self.pointList[1][1])

    def get_rect(self):
        return pygame.Rect(self.upperLeft[0]+self.x,self.upperLeft[1]+self.y, self._size, self._size)
