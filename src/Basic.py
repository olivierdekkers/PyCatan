import pygame
import pathlib
import os
from images.imageloader import ImageLoader
from circle import Circle, Handelaar, Vikings
import board
from math import cos, sin, ceil


pygame.init()
screenInfo = pygame.display.Info()

pi2 = 2 * 3.14159265358979
screen = pygame.display.set_mode([screenInfo.current_w, screenInfo.current_h])
imagePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./images/socPictures")
imLoader = ImageLoader(imagePath)
running = True

playingField, cornerNodes, centers, roads= board.fourPersonPlayingfield(int(screenInfo.current_w/2), int(screenInfo.current_h/2), imLoader, 150)

def Players(playerNames = [("socVincent", (23,227,101)), ("socLewisSr", (106,142,226)), ("socPlatte", (249,197,216)), ("socStrakke", (23,227,217))]):
    i = 0
    while True:
        yield playerNames[i]
        i+=1
        i %=4
size = screenInfo.current_h /2

nodeOptions = [
            (
                int(cos(i / 6 * pi2) * size + screenInfo.current_w/2) - 75,
                int(sin(i / 6 * pi2) * size + size)-int(size/10)
            )
            for i in range(0, 6)
        ]

ports = []
for location, name in [((655, 600), 'steen'),( (655, 1010), 'threeone'),( (1000, 1200),'threeone'),( (1460, 1200),'scheep'),( (1805.0 ,1012.5),'threeone'),( (1825.0 ,600),'ironOre'),( (1580.0, 215.5),'grain'),( (1230, 30),'threeone'),( (900, 220),'wood')]:
    image = getattr(imLoader, name)
    ci = Circle(location[0], location[1], 150/6, image)
    ci.render()
    ports.append(ci)


for field in playingField:
    if field.color == (222, 184, 135):
        image = getattr(imLoader, "vikings")
        ci = Vikings(field.x+150/4, field.y+150/4, 150/6, image)
        ci.name = "vikings"
        ci.render()
        vikings = ci
        image = getattr(imLoader, "handelaar")
        ci = Handelaar(field.x+150, field.y+150/4, 150/6, image)
        ci.name = "handelaar"
        ci.render()
        handelaar = ci


players = Players()
player, color = next(players)
boat = imLoader.boat

selectedItem = None
actionNodes = []
button_pressed = 0

selectableItems = [handelaar, vikings]
selectableItems.extend(centers)
selectableItems.extend(cornerNodes)
selectableItems.extend(roads)

def checkColide(item):
    return item.get_rect().collidepoint(pygame.mouse.get_pos())



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            button_pressed = 0
        if event.type == pygame.MOUSEBUTTONDOWN and not button_pressed:
            mousePos = pygame.mouse.get_pos()
            button_pressed = 1
            if event.button == 1: # left
                if not selectedItem:
                    for item in selectableItems:
                        if checkColide(item):
                            selectedItem, actionNodes = item.select(player, nodeOptions)
                            break
                    else:
                        player, color = next(players)
                else:
                    try:
                        selectedItem.clicked(mousePos,player,None,color)
                    except:  # it must be a center
                        possibleItems = centers[:]
                        possibleItems.extend(actionNodes)
                        for item in possibleItems:
                            if checkColide(item):
                                item.clicked(mousePos,player,selectedItem,color)
                                break
                        else:
                            player, color= next(players)
                    actionNodes = []
                    selectedItem = None

    screen.fill(color)
    screen.set_colorkey((255, 255, 255))
    for tile in playingField:
        tile.render()

    screen.blits([(tile._image, (int(tile.x), int(tile.y))) for tile in playingField])
    screen.blits([(node._image, (int(node.x), int(node.y))) for node in centers])
    screen.blits([(node._image, (int(node.x), int(node.y))) for node in cornerNodes])
    screen.blits([(node._image, (int(node.x), int(node.y))) for node in roads])
    screen.blits([(node._image, (int(node.x), int(node.y))) for node in ports])
    screen.blit(handelaar._image, (handelaar.x, handelaar.y))
    screen.blit(vikings._image, (vikings.x, vikings.y))

    if actionNodes:
        screen.blits([(item._image, (item.x, item.y)) for item in actionNodes])

    pygame.display.update()

pygame.quit()
