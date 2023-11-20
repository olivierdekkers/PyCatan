import random
from circle import Circle, CornerNode, ActionNode, Road, Center
from hex import Hex
from math import cos, sin



COLORDICT = {
        'grain': (202, 184, 162),
        'weiland': (163, 232, 140),
        'forrest': (2, 94, 4),
        'mountain': (255, 140, 0),
        'mine': (142, 141, 145),
        'desert': (222, 184, 135)
        }
pi2 = 2 * 3.14159265358979

def fourPersonPlayingfield(centerX, centerY, images, size=100):
    AllFields = ['grain']*4+['weiland']*4+['forrest']*4+['mountain']*3+['mine']*3+['desert']
    random.shuffle(AllFields)

    hexFields = []
    # return [Hex(100, getattr(images, 'grain'), COLORDICT['grain'], 1)]
    for field in AllFields:
        image = getattr(images, field)
        color = COLORDICT[field]
        hexFields.append(Hex(size, image, color))


    columns = [3,4,5,4,3]
    board = []
    fieldCount = 0
    x = 0
    y = 0
    for columnCount, column in enumerate(columns):
        for count in range(column):
            tile = hexFields[fieldCount]
            board.append(tile.translate(x,y))
            fieldCount += 1
            y += tile.height
        try:
            if columns[columnCount+1] < column:
                x,y = board[-columns[columnCount]].bottomRight
                y -= tile.height/2 + board[0].upperRight[1]
            else:
                x,y = board[-columns[columnCount]].upperRight
                y -= tile.height/2 + board[0].upperRight[1]
        except:
            pass
    midleTile = board[9]
    translateX = centerX-size + board[0].x - midleTile.x
    translateY = centerY - midleTile.height/2 + board[0].y - midleTile.y
    for tile in board:
        tile.translate(translateX, translateY)

    #reorder boards
    if random.randint(0,10) % 2:
        boardSequence = [5, 2, 8, 3, 6, 10, 12, 9, 11, 4, 8, 10, 4, 9, 5, 6, 3, 11]
    else:
        boardSequence = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
    orderedBoard = [board[0], board[1], board[2], board[6], board[11], board[15], board[18], board[17], board[16], board[12], board[7], board[3], board[4], board[5], board[10], board[14], board[13], board[8], board[9]]
    corners = []
    roadCoordinates = []
    cornerNodes = []
    centers = []
    roads = []
    for tile in orderedBoard:
        corners.extend([point for point in tile.pointList if point not in corners])

        for index1 in range(len(tile.pointList)):
            index2 = (index1 + 1) % 6
            middleX = (tile.pointList[index1][0] + tile.pointList[index2][0])/2
            middleY = (tile.pointList[index1][1] + tile.pointList[index2][1])/2
            if (middleX, middleY) not in roadCoordinates:
                roadCoordinates.append((middleX, middleY))

        if tile.color!=(222, 184, 135):
            circ = Center(tile.x+size/2, tile.y+size*2/5, size/4, color=(254,254,254), number=boardSequence.pop(0))
            circ.render()
            centers.append(circ)
    for corner in corners:
        circ = CornerNode(corner[0]-size/2, corner[1]-size/2, size/4, color=(125,125,125))
        circ.render()
        cornerNodes.append(circ)
    for roadCoord in roadCoordinates:
        circ = Road(roadCoord[0]-size/4, roadCoord[1]-size/4, size/8, color=(0, 0, 0))
        circ.render()
        roads.append(circ)

    return orderedBoard, cornerNodes, centers, roads
