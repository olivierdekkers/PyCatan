import pygame
import os
from math import cos, sin, ceil
from images.imageloader import ImageLoader
imagePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./images/socPictures")
imLoader = ImageLoader(imagePath)

class Circle:

    def __init__(self, x, y, size, image=None, color=(255,255,255), number=None, refItem=None):
        self.x = x
        self.y = y
        self.size = size
        self.background = image
        self._number = number
        self.color = color
        self.name = "default"
        self._image = None
        self._refItem = refItem

    def draw(self, surface):
        surface.blit(self._image, (self.x, self.y))
        return surface

    def render(self):
        if self.background:
            backgroundSize = self.size/3 if self.name.endswith("helmet") or self.name.endswith("wall") else self.size
            if backgroundSize != self.size:
                originalImage = self._image
            self._image = pygame.transform.scale(self.background, (int(4*backgroundSize),int(4*backgroundSize)))
            self._image.set_colorkey((255,255,255))
            mask = pygame.Surface(self._image.get_rect().size)
            mask.fill((255,255,255,0)) # everything covered with white will become invisible
            # draw hole in mask?
            mask.set_colorkey((10,10,10))  # circle with same collor will make hole
            pygame.draw.circle(
                mask,
                (10, 10, 10),
                (backgroundSize*2, backgroundSize*2),
                backgroundSize*1.5
                )
            self._image.blit(mask, (0,0))
            pygame.draw.circle(
                self._image,
                self.color,
                (self.size*2, self.size*2),
                self.size*1.5,
                2
                )
            if backgroundSize != self.size and originalImage:
                originalImage.blit(self._image, (0,0))
                self._image = originalImage
        else:
            mask = pygame.Surface((self.size*4, self.size*4))
            mask.set_colorkey((0, 0, 0))
            mask.fill((0,0,0, 0))

            pygame.draw.circle(
                mask,
                self.color,
                (self.size*2, self.size*2),
                self.size
                )
            if self._number is not None:
                font = pygame.font.SysFont('chalkduster.ttf', 40)
                text = font.render(str(self._number), True, (1,1,1))
                rect = text.get_rect()
                rect.center = (self.size*2, self.size*2)
                mask.blit(text, rect)
            self._image = mask

    def translate(self, x,y):
        self.x += x
        self.y += y
        return self

    def get_rect(self):
        return pygame.Rect(self.x+self.size/1.3, self.y+self.size/1.3, self.size*2.5, self.size*2.5)

    def select(self, player, nodeOptions):
        return self, []

class CornerNode(Circle):

    def select(self, player, nodeOptions):
        actionNodes = []
        for typ, (x, y) in zip(["city", "village", "metropool", "knight1", "knight2", "knight3"], nodeOptions):
            if player+typ == self.name and typ.startswith('knight'):
                typ = "helmet"
            elif player+typ == self.name:
                typ = "wall"
            image = getattr(imLoader, player+typ)
            ci = ActionNode(x, y, self.size, image, refItem=self)
            ci.name = player+typ
            ci.render()
            actionNodes.append(ci)
        return self, actionNodes

class ActionNode(Circle):

    def clicked(self, mousePosition, player, clickedItem, color):
        self._refItem.background = self.background
        self._refItem.color = color
        self._refItem.name = self.name
        self._refItem.render()

class Road(Circle):

    def select(self, player, nodeOptions):
        if self.background:
            self.background = None
            self.render()
        else:
            image = getattr(imLoader, player+"road")
            self.background = image
            self.render()
        return None, []

class Vikings(Circle):

    def clicked(self, mousePosition, player, clickedItem, color):
        self.x = pygame.mouse.get_pos()[0] -150/3
        self.y = pygame.mouse.get_pos()[1] - 150/3

class Handelaar(Vikings):
    pass

class Center(Circle):

    def clicked(self, mousePosition, player, clickedItem, color):
        print(clickedItem)
        clickedItem.x, self.x = self.x, clickedItem.x
        clickedItem.y, self.y = self.y, clickedItem.y
