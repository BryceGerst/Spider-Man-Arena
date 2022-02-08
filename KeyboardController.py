# This was created to emulate controller inputs in the event that only
# one keyboard is available for use
import pygame, math

ROTATE_STRENGTH = 0.05

class KeyboardController:
    def __init__(self, ccwRotateKey, cwRotateKey, shootKey, leftKey, rightKey, upKey, downKey, dashKey, swapKey):
        self.aimAngle = 0
        
        self.ccwRotateKey = ccwRotateKey
        self.cwRotateKey = cwRotateKey
        self.shootKey = shootKey
        self.leftKey = leftKey
        self.rightKey = rightKey
        self.upKey = upKey
        self.downKey = downKey
        self.dashKey = dashKey
        self.swapKey = swapKey

    def get_button(self, buttonNum):
        if buttonNum == 0:
            return pygame.key.get_pressed()[self.swapKey]
        elif buttonNum == 1:
            return pygame.key.get_pressed()[self.ccwRotateKey] # this is the unselect key
        elif buttonNum == 4:
            return pygame.key.get_pressed()[self.ccwRotateKey] # this is some map pick key
        elif buttonNum == 5:
            return pygame.key.get_pressed()[self.cwRotateKey] # this is another map pick key

    def get_axis(self, axisNum):
        keys = pygame.key.get_pressed()
        if axisNum == 0:
            if keys[self.rightKey]:
                return 1
            elif keys[self.leftKey]:
                return -1
            else:
                return 0
        elif axisNum == 1:
            if keys[self.upKey]:
                return -1
            elif keys[self.downKey]:
                return 1
            else:
                return 0
        elif axisNum == 2:
            if keys[self.ccwRotateKey]:
                self.aimAngle += ROTATE_STRENGTH
            if keys[self.cwRotateKey]:
                self.aimAngle -= ROTATE_STRENGTH
            return 2 * math.sin(self.aimAngle)
        elif axisNum == 3:
            if keys[self.ccwRotateKey]:
                self.aimAngle += ROTATE_STRENGTH
            if keys[self.cwRotateKey]:
                self.aimAngle -= ROTATE_STRENGTH
            return 2 * math.cos(self.aimAngle)
        elif axisNum == 4:
            if keys[self.dashKey]:
                return 1
            else:
                return 0
        elif axisNum == 5:
            if keys[self.shootKey]:
                return 1
            else:
                return 0

    def get_hat(self, hatNum):
        return [0,0,0,0]
