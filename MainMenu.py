# This file handles the utility and displaying of the main menu

import pygame, Colors

def run(displayInfo):
    # Unpackaging all of the information
    screen = displayInfo[0]
    clock = displayInfo[1]
    screenW = displayInfo[2]
    screenH = displayInfo[3]
    fps = displayInfo[4]
    # Main menu loop
    inMenu = True
    mouseClick = False
    while inMenu:
        mouseX, mouseY = pygame.mouse.get_pos()
        # Checks if mouse is clicked
        if mouseClick:
            return 2
        screen.fill(Colors.GREY)
        pygame.display.update()
        mouseClick = False
        # Exit code
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseClick = True
            if event.type == pygame.QUIT or pygame.key.get_pressed()[27]: # key 27 is escape
                inMenu = False
                return -1
