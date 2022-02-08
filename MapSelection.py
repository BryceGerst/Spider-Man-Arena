import pygame, Maps, Colors, random
from KeyboardController import *

def run(displayInfo):
    screen = displayInfo[0]
    clock = displayInfo[1]
    screenW = displayInfo[2]
    screenH = displayInfo[3]
    fps = displayInfo[4]

    font = pygame.font.Font('freesansbold.ttf', 64) 
  
    p1ChooseText = font.render('Player 1 Ban', True, Colors.BLUE)
    p2ChooseText = font.render('Player 2 Ban', True, Colors.RED)

    bo5Text = font.render('BEST of 5', True, Colors.BLACK)
    bo9Text = font.render('BEST of 9', True, Colors.BLACK)
    
    textCoords = ((screenW // 2) - (p1ChooseText.get_width() // 2), 0)

    previewWidth = screenW // 6
    previewHeight = screenH // 5

    widthUnit = previewWidth // 6
    midH = screenH // 2
    mapH = midH - (previewHeight // 2)

    map1Preview = Maps.loadMap1((previewWidth, previewHeight))[1]
    map2Preview = Maps.loadMap2((previewWidth, previewHeight))[1]
    map3Preview = Maps.loadMap3((previewWidth, previewHeight))[1]
    map4Preview = Maps.loadMap4((previewWidth, previewHeight))[1]
    map5Preview = Maps.loadMap5((previewWidth, previewHeight))[1]
    preview1Rect = pygame.Rect(widthUnit, mapH, previewWidth, previewHeight)
    preview2Rect = pygame.Rect(2*widthUnit+previewWidth, mapH, previewWidth, previewHeight)
    preview3Rect = pygame.Rect(3*widthUnit+2*previewWidth, mapH, previewWidth, previewHeight)
    preview4Rect = pygame.Rect(4*widthUnit+3*previewWidth, mapH, previewWidth, previewHeight)
    preview5Rect = pygame.Rect(5*widthUnit+4*previewWidth, mapH, previewWidth, previewHeight)
    screen.fill(Colors.WHITE)
    screen.blit(map1Preview, (widthUnit, mapH))
    screen.blit(map2Preview, (2*widthUnit+previewWidth, mapH))
    screen.blit(map3Preview, (3*widthUnit+2*previewWidth, mapH))
    screen.blit(map4Preview, (4*widthUnit+3*previewWidth, mapH))
    screen.blit(map5Preview, (5*widthUnit+4*previewWidth, mapH))

    picking = True
    mapsBanned = 0
    totalMaps = 5
    mouseWasDown = True
    lastX = 0

    map1Banned = False
    map2Banned = False
    map3Banned = False
    map4Banned = False
    map5Banned = False

    player1Picking = True
    mapOn = 1
    
    p1First = random.randint(0, 1)
    usingControllers = (pygame.joystick.get_count() == 2)
    if p1First == 1:
        if usingControllers:
            cont1 = pygame.joystick.Joystick(0)
            cont2 = pygame.joystick.Joystick(1)
        else:
            cont1 = KeyboardController(pygame.K_q, pygame.K_e, pygame.K_SPACE, pygame.K_a,
                                        pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT, pygame.K_x)
            cont2 = KeyboardController(pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_LEFT,
                                        pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT, pygame.K_m)
    else:
        if usingControllers:
            cont2 = pygame.joystick.Joystick(0)
            cont1 = pygame.joystick.Joystick(1)
        else:
            cont2 = KeyboardController(pygame.K_q, pygame.K_e, pygame.K_SPACE, pygame.K_a,
                                        pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT, pygame.K_x)
            cont1 = KeyboardController(pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_LEFT,
                                        pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT, pygame.K_m)

    lastFrameToggle = False
    bestOfToggle = True

    
    while picking:
        if (cont1.get_button(4) or cont2.get_button(4) or cont1.get_button(5) or cont2.get_button(5)) and not lastFrameToggle:
            bestOfToggle = not bestOfToggle
        lastFrameToggle = (cont1.get_button(4) or cont2.get_button(4) or cont1.get_button(5) or cont2.get_button(5))
        if player1Picking:
            contUsing = cont1
        else:
            contUsing = cont2
        for event in pygame.event.get():
              # This if statement checks when to stop running the game code
             if event.type == pygame.QUIT or pygame.key.get_pressed()[27]: # key 27 is escape
                 picking = False
                 return -1, 0, 0
        currentX = contUsing.get_axis(0)
        if lastX > -0.8 and currentX < -0.8:
            if mapOn != 1:
                mapOn -= 1
            else:
                mapOn = 5
        if lastX < 0.8 and currentX > 0.8:
            if mapOn != 5:
                mapOn += 1
            else:
                mapOn = 1
        
        if not mouseWasDown and contUsing.get_button(0):
            if not map1Banned and mapOn == 1:
                map1Banned = True
                mapsBanned += 1
                if mapsBanned == 1:
                    player1Picking = False
                elif mapsBanned == 3:
                    player1Picking = True
            elif not map2Banned and mapOn == 2:
                map2Banned = True
                mapsBanned += 1
                if mapsBanned == 1:
                    player1Picking = False
                elif mapsBanned == 3:
                    player1Picking = True
            elif not map3Banned and mapOn == 3:
                map3Banned = True
                mapsBanned += 1
                if mapsBanned == 1:
                    player1Picking = False
                elif mapsBanned == 3:
                    player1Picking = True
            elif not map4Banned and mapOn == 4:
                map4Banned = True
                mapsBanned += 1
                if mapsBanned == 1:
                    player1Picking = False
                elif mapsBanned == 3:
                    player1Picking = True
            elif not map5Banned and mapOn == 5:
                map5Banned = True
                mapsBanned += 1
                if mapsBanned == 1:
                    player1Picking = False
                elif mapsBanned == 3:
                    player1Picking = True
        if mapsBanned >= totalMaps - 1:
            picking = False
        mouseWasDown = contUsing.get_button(0)
        lastX = contUsing.get_axis(0)
        screen.fill(Colors.WHITE)
        if mapOn == 1:
            pygame.draw.rect(screen, Colors.YELLOW, preview1Rect.inflate(10,10))
        elif mapOn == 2:
            pygame.draw.rect(screen, Colors.YELLOW, preview2Rect.inflate(10,10))
        elif mapOn == 3:
            pygame.draw.rect(screen, Colors.YELLOW, preview3Rect.inflate(10,10))
        elif mapOn == 4:
            pygame.draw.rect(screen, Colors.YELLOW, preview4Rect.inflate(10,10))
        elif mapOn == 5:
            pygame.draw.rect(screen, Colors.YELLOW, preview5Rect.inflate(10,10))
        
        screen.blit(map1Preview, (widthUnit, mapH))
        screen.blit(map2Preview, (2*widthUnit+previewWidth, mapH))
        screen.blit(map3Preview, (3*widthUnit+2*previewWidth, mapH))
        screen.blit(map4Preview, (4*widthUnit+3*previewWidth, mapH))
        screen.blit(map5Preview, (5*widthUnit+4*previewWidth, mapH))
        if map1Banned:
            pygame.draw.rect(screen, Colors.RED, preview1Rect)
        if map2Banned:
            pygame.draw.rect(screen, Colors.RED, preview2Rect)
        if map3Banned:
            pygame.draw.rect(screen, Colors.RED, preview3Rect)
        if map4Banned:
            pygame.draw.rect(screen, Colors.RED, preview4Rect)
        if map5Banned:
            pygame.draw.rect(screen, Colors.RED, preview5Rect)

        if bestOfToggle:
            screen.blit(bo5Text, (0,0))
        else:
            screen.blit(bo9Text, (0,0))
            
        if p1First:
            if player1Picking:
                screen.blit(p1ChooseText, textCoords)
            else:
                screen.blit(p2ChooseText, textCoords)
        else:
            if player1Picking:
                screen.blit(p2ChooseText, textCoords)
            else:
                screen.blit(p1ChooseText, textCoords)
        pygame.display.update()
        
    mapNum = -1
    if not map1Banned:
        mapNum = 1
    elif not map2Banned:
        mapNum = 2
    elif not map3Banned:
        mapNum = 3
    elif not map4Banned:
        mapNum = 4
    elif not map5Banned:
        mapNum = 5
        
    if bestOfToggle:
        bo = 5
    else:
        bo = 9
    return 2, mapNum, bo
