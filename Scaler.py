# This file will adjust image sizes, coordinates, and more to work on displays of all sizes
# By default, values are intended for 1920 by 1080 screens
import pygame

def rint(num): #rounded int
    newNum = int(num + 0.5)
    return newNum

class Scaler:
    def __init__(self, screenW, screenH, maxWidth = 1920, maxHeight = 1080):
        self.maxW = maxWidth
        self.maxH = maxHeight
        self.wRatio = maxWidth / screenW
        self.hRatio = maxHeight / screenH
        self.defaultSize = self.wRatio == 1 and self.hRatio == 1 # if they are both 1, the screen size is 1920 by 1080
            
    def scaleImage(self, image):
        if self.defaultSize:
            return image
        else:
            oldWidth, oldHeight = pygame.Surface.get_size(image)
            newWidth =  rint(oldWidth * self.wRatio) # casts to an int because a sprite can't be 10.3 pixels wide, for example
            newHeight = rint(oldHeight * self.hRatio)
            newImage = pygame.transform.scale(image, (newWidth, newHeight))
            return newImage

    def scaleRect(self, rect):
        if self.defaultSize:
            return rect
        else:
            coord = rect.left, rect.top
            newCoord = self.scalePoint(coord[0], coord[1])
            oldWidth, oldHeight = rect.width, rect.height
            newWidth =  rint(oldWidth * self.wRatio) # casts to an int because a sprite can't be 10.3 pixels wide, for example
            newHeight = rint(oldHeight * self.hRatio)
            newRect = pygame.Rect(newCoord, (newWidth, newHeight))
            return newRect

    def scalePoint(self, pointX, pointY):
        if self.defaultSize:
            return pointX, pointY
        else:
            newX = rint(pointX * self.hRatio)
            newY = rint(pointY * self.wRatio)
            return newX, newY
