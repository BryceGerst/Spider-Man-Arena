import pygame, Colors
import Character as c

def draw(screen, sprite, pos):
    halfW = sprite.get_width() // 2
    halfH = sprite.get_height() // 2
    screen.blit(sprite, (pos[0] - halfW, pos[1] - halfH))

def run(displayInfo):
    screen = displayInfo[0]
    clock = displayInfo[1]
    screenW = displayInfo[2]
    screenH = displayInfo[3]
    fps = displayInfo[4]

    font = pygame.font.Font('freesansbold.ttf', 64)


    previewWidth = screenW // 8
    previewHeight = previewWidth

    widthUnit = int(previewWidth * 1.5)
    inflateUnit = previewWidth // 4
    midH = screenH // 2
    mapH = midH - (previewHeight // 2)

    orderChars = [c.spidey, c.peter, c.ironman, c.goblin, c.poggle, c.lemon, c.r2, c.babynut, c.chrome, c.bird]

    allCharPreviews = []
    allCharNames = []
    for char in orderChars:
        allCharPreviews.append(pygame.transform.scale(char.sprite, (previewWidth, previewHeight)))
        allCharNames.append(font.render(char.name, True, char.getColor()))

    preview1Rect = pygame.Rect(widthUnit, mapH, previewWidth, previewHeight)
    preview2Rect = pygame.Rect(screenW - widthUnit - previewWidth, mapH, previewWidth, previewHeight)
    preview1Rect = preview1Rect.inflate(inflateUnit, inflateUnit)
    preview2Rect = preview2Rect.inflate(inflateUnit, inflateUnit)
    screen.fill(Colors.WHITE)

    

    lastX = 0

    p1CharSelected = -1
    p2CharSelected = -1
    p1CharOn = 1
    p2CharOn = 1

    cont1 = pygame.joystick.Joystick(0)
    cont2 = pygame.joystick.Joystick(1)

    lastX = [0, 0]
    mouseWasDown = [True, True]
    bWasDown = [True, True]
    picking = True
    
    while picking:
        for event in pygame.event.get():
              # This if statement checks when to stop running the game code
             if event.type == pygame.QUIT or pygame.key.get_pressed()[27]: # key 27 is escape
                 picking = False
                 return -1, -1, -1, -1, -1
        for i in range(2):
            if i == 0:
                cont = cont1
            else:
                cont = cont2
            if cont.get_button(0) and not mouseWasDown[i]:
                if i == 0:
                    p1CharSelected = p1CharOn
                else:
                    p2CharSelected = p2CharOn
            if cont.get_button(1) and not bWasDown[i]:
                if i == 0:
                    p1CharSelected = -1
                else:
                    p2CharSelected = -1
            if i == 0:
                charSelected = p1CharSelected
            else:
                charSelected = p2CharSelected
            currentX = cont.get_axis(0)
            if charSelected == -1:
                if lastX[i] > -0.8 and currentX < -0.8:
                    if i == 0:
                        if p1CharOn != 1:
                            p1CharOn -= 1
                        else:
                            p1CharOn = len(allCharPreviews)
                    else:
                        if p2CharOn != 1:
                            p2CharOn -= 1
                        else:
                            p2CharOn = len(allCharPreviews)
                if lastX[i] < 0.8 and currentX > 0.8:
                    if i == 0:
                        if p1CharOn != len(allCharPreviews):
                            p1CharOn += 1
                        else:
                            p1CharOn = 1
                    else:
                        if p2CharOn != len(allCharPreviews):
                            p2CharOn += 1
                        else:
                            p2CharOn = 1
            mouseWasDown[i] = cont.get_button(0)
            bWasDown[i] = cont.get_button(1)
            lastX[i] = cont.get_axis(0)
            
        
        screen.fill(Colors.WHITE)

        if p1CharSelected == -1:
            pygame.draw.rect(screen, Colors.RED, preview1Rect)
        else:
            pygame.draw.rect(screen, Colors.GREEN, preview1Rect)

        if p2CharSelected == -1:
            pygame.draw.rect(screen, Colors.RED, preview2Rect)
        else:
            pygame.draw.rect(screen, Colors.GREEN, preview2Rect)

        p1CharPreview = allCharPreviews[p1CharOn - 1]
        p1Text = font.render(orderChars[p1CharOn-1].name, True, orderChars[p1CharOn-1].getColor())
        screen.blit(p1CharPreview, (widthUnit, mapH))
        draw(screen, p1Text, (widthUnit + (previewWidth // 2), int((7/4)*mapH)))

        p2CharPreview = allCharPreviews[p2CharOn - 1]
        p2Text = font.render(orderChars[p2CharOn-1].name, True, orderChars[p2CharOn-1].getColor())
        screen.blit(p2CharPreview, (screenW - widthUnit - previewWidth, mapH))
        draw(screen, p2Text, (screenW - widthUnit - (previewWidth // 2), int((7/4)*mapH)))


        if p1CharSelected != -1 and p2CharSelected != -1:
            picking = False
        
        pygame.display.update()

    p1Balls = Colors.WHITE
    p2Balls = Colors.WHITE

    p1Selected = orderChars[p1CharSelected - 1]
    p2Selected = orderChars[p2CharSelected - 1]
        
    return 1, p1Selected, p2Selected, p1Balls, p2Balls
