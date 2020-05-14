# This file handles the primary gameplay

import pygame, Colors, Maps, Scaler, math, random

pygame.mixer.init()
noiseChannel = pygame.mixer.Channel(2)
p1ShootChannel = pygame.mixer.Channel(3)
p2ShootChannel = pygame.mixer.Channel(4)

def move(pos, direction, distance, hitbox, gameMap):
    posX = pos[0]
    posY = pos[1]
    mag = math.hypot(direction[0], direction[1])
    if mag >= 0.1:
        direct = math.atan2(direction[1], direction[0])
        dirX = math.cos(direct)
        dirY = math.sin(direct)
##        if mag > 1:
##            dirX = direction[0] / mag
##            dirY = direction[1] / mag
##        else:
##            dirX = direction[0]
##            dirY = direction[1]
    else:
        return pos
    posX = int(posX + (dirX * distance) + 0.5)
    posY = int(posY + (dirY * distance) + 0.5)

    xBad = True
    testXCircle = properHitbox(hitbox, (posX, pos[1]))
    for coord in testXCircle:
        try:
            xBad = gameMap.get_at(coord) == Colors.BLACK
        except:
            xBad = True
        if xBad:
            posX = pos[0]

    yBad = True
    testYCircle = properHitbox(hitbox, (pos[0], posY))
    for coord in testYCircle:
        try:
            yBad = gameMap.get_at(coord) == Colors.BLACK
        except:
            yBad = True
        if yBad:
            posY = pos[1]

    return int(posX + 0.5), int(posY + 0.5)

def draw(screen, sprite, pos):
    halfW = sprite.get_width() // 2
    halfH = sprite.get_height() // 2
    screen.blit(sprite, (pos[0] - halfW, pos[1] - halfH))

def circleHitbox(radius):
    pixels = set()
    pixels.add((0,0))
    currentTheta = 0
    while currentTheta < math.pi * 2:
        xComp = radius * math.cos(currentTheta)
        yComp = radius * math.sin(currentTheta)
        newPixel = (rint(xComp), rint(yComp))
        pixels.add(newPixel)
        currentTheta += 0.05
    return pixels

def properHitbox(hitbox, pos):
    posX = pos[0]
    posY = pos[1]
    newCoord = set()
    for coord in hitbox:
        newCoord.add((coord[0] + posX, coord[1] + posY))
    return newCoord

def rint(num):
    return int(num+0.5)

def closeInMap(gameMap, perc):
    totalWidth = gameMap.get_width()
    totalHeight = gameMap.get_height()
    sideBarWidth = rint(perc * (totalWidth / 2))
    topBarHeight = rint(perc * (totalHeight / 2))
    tB = pygame.Surface((totalWidth, topBarHeight))
    tB.set_alpha(128)
    tB.fill(Colors.BLUE)
    gameMap.blit(tB, (0,0))
    bB = pygame.Surface((totalWidth, topBarHeight))
    bB.set_alpha(128)
    bB.fill(Colors.BLUE)
    gameMap.blit(bB, (0,totalHeight - topBarHeight))
    lB = pygame.Surface((sideBarWidth, totalHeight - (2*topBarHeight)))
    lB.set_alpha(128)
    lB.fill(Colors.BLUE)
    gameMap.blit(lB, (0,topBarHeight))
    rB = pygame.Surface((sideBarWidth, totalHeight - (2*topBarHeight)))
    rB.set_alpha(128)
    rB.fill(Colors.BLUE)
    gameMap.blit(rB, (totalWidth - sideBarWidth, topBarHeight))

    return sideBarWidth, totalWidth - sideBarWidth, topBarHeight, totalHeight - topBarHeight
    

def run(displayInfo, score, char1, char2, mapNum, p1BallColor, p2BallColor, boNum):
    p1BallColor = Colors.WHITE
    p2BallColor = Colors.WHITE
    sprite1 = char1.sprite
    sprite2 = char2.sprite
    pygame.mouse.set_visible(False)
    # Unpackaging all of the information
    screen = displayInfo[0]
    clock = displayInfo[1]
    screenW = displayInfo[2]
    screenH = displayInfo[3]
    fps = displayInfo[4]
    # Main gameplay
    inGameplay = True
    mouseClick = False
    matchEnd = False
    playerObjs = []
    X = 0
    Y = 1
    sc = Scaler.Scaler(screenW, screenH)
    if mapNum == 1:
        map1,map2 = Maps.loadMap1((screenW, screenH))
    elif mapNum == 2:
        map1,map2 = Maps.loadMap2((screenW, screenH))
    elif mapNum == 3:
        map1,map2 = Maps.loadMap3((screenW, screenH))
    elif mapNum == 4:
        map1,map2 = Maps.loadMap4((screenW, screenH))
    elif mapNum == 5:
        map1,map2 = Maps.loadMap5((screenW, screenH))
    p1Score = score[0]
    p2Score = score[1]
    p1DispScore = pygame.image.load('Images/bo' + str(boNum) + '-' + str(p1Score) + '.png')
    p2DispScore = pygame.image.load('Images/bo' + str(boNum) + '-' + str(p2Score) + '.png')
    p1DispScore  = pygame.transform.scale(p1DispScore, (rint(screenW / 8), rint(screenH / 13.5)))
    p2DispScore  = pygame.transform.scale(p2DispScore, (rint(screenW / 8), rint(screenH / 13.5)))

    playerRadius = screenW // 50
    lengthUnit = playerRadius // 7.5 # 20
    sprite1 = pygame.transform.scale(sprite1, (playerRadius * 2, playerRadius * 2))
    sprite2 = pygame.transform.scale(sprite2, (playerRadius * 2, playerRadius * 2))
    p1Pos = (int(playerRadius + lengthUnit * 20), int(screenH / 2))
    p1 = Player(p1Pos, playerRadius, sprite1, lengthUnit, map1, p1BallColor, 0, 0)
    p2Pos = (int(screenW - playerRadius - lengthUnit * 20), int(screenH / 2))
    p2 = Player(p2Pos, playerRadius, sprite2, lengthUnit, map1, p2BallColor, 1, 0)
    deadzone = 0.9 # 0.9 normally
    moveDeadzone = 0.3 # 0 normally I guess
    triggerDeadzone = 0.4

    helpEnabled = False #True
    helper1 = Bot(p1, p2, map1)
    helper2 = Bot(p2, p1, map1)

    players = []
    players.append(p1)
    players.append(p2)

    projectiles = []

    frames = 0
    maxFrames = 3600
    minFrames = 600
    maxPerc = 0.5
    #maxPerc = 0.6
    borderInfo = closeInMap(screen, 0)

    banter1Played = False
    banter2Played = False
    doingBanter = (score[0] == 0 and score[1] == 0)

    p1ZoomScreen = pygame.Surface((screenW, screenH))
    p1ZoomScreen.fill(Colors.GREY)
    bigSprite1 = pygame.transform.scale(sprite1, ((screenH, screenH)))
    bigSprite1 = pygame.transform.rotate(bigSprite1, 270)
    draw(p1ZoomScreen, bigSprite1, (screenW // 2, screenH // 2))

    p2ZoomScreen = pygame.Surface((screenW, screenH))
    p2ZoomScreen.fill(Colors.GREY)
    bigSprite2 = pygame.transform.scale(sprite2, ((screenH, screenH)))
    bigSprite2 = pygame.transform.rotate(bigSprite2, 90)
    draw(p2ZoomScreen, bigSprite2, (screenW // 2, screenH // 2))

    while doingBanter:
        if not banter1Played:
            char1.playBanterOn(noiseChannel)
            banter1Played = True
        if banter1Played and not noiseChannel.get_busy() and not banter2Played:
            char2.playBanterOn(noiseChannel)
            banter2Played = True
        else:
            screen.blit(p1ZoomScreen, (0,0))
        if banter2Played and noiseChannel.get_busy():
            screen.blit(p2ZoomScreen, (0,0))
        elif banter1Played and banter2Played and not noiseChannel.get_busy():
            doingBanter = False
        pygame.display.update()
        clock.tick(60)
    
    while inGameplay:
        controllersConnected = pygame.joystick.get_count()
        if controllersConnected != 2:
            # pause game
            return -1
        else:
            # Checks if mouse is clicked
            if matchEnd:
                return 2
            # Player controls
            inputs = pygame.key.get_pressed()
            moveStickPos = []
            try:
                lastAimPos = [aimStickPos[0], aimStickPos[1]]
            except:
                lastAimPos = [(0, 0), (0, 0)]
            aimStickPos = []
            triggerValues = []
            button1 = []
            downHat = []
            for i in range(controllersConnected):
                controller = pygame.joystick.Joystick(i)
                controller.init()
                movePos = (controller.get_axis(0), controller.get_axis(1))
                if math.hypot(movePos[0], movePos[1]) > moveDeadzone:
                    moveStickPos.append(movePos)
                else:
                    moveStickPos.append((0,0))
                    
                aimPos = (controller.get_axis(3), controller.get_axis(4)) # 3, 4
                if math.hypot(aimPos[0], aimPos[1]) > deadzone:
                    aimStickPos.append(aimPos)
                else:
                    aimStickPos.append(lastAimPos[i])
                downHat.append(controller.get_hat(0)[1] == -1)
                triggerValues.append(controller.get_axis(2))
                button1.append(controller.get_button(0))


            
            # Draws background
            screen.blit(map1, (0,0))
            # Updates players
            for i in range(len(players)):
                
                player = players[i]
                if helpEnabled and player.helpToggle and i == 1:
                    if i == 0:
                        helper1.update(projectiles)
                    else:
                        helper2.update(projectiles)
                projectile = player.update(button1[i], aimStickPos[i], triggerValues[i], moveStickPos[i], downHat[i], borderInfo)
                #player.drawToScreen(screen)
                if projectile != 0:
                    if i == 0:
                        char1.playShootOn(p1ShootChannel)
                    else:
                        char2.playShootOn(p2ShootChannel)
                    projectiles.append(projectile)
                # help used to be here
                
            # Updates projectiles
            p1hb = properHitbox(players[0].hitbox, players[0].pos)
            p2hb = properHitbox(players[1].hitbox, players[1].pos)
            for i in range(len(projectiles)):
                if i < len(projectiles):
                    projectile = projectiles[i]
                    result = projectile.update(map1, players)
                    if result == -1:
                        projectiles.pop(i)
                        i -= 1
                    elif result > 0:
                        players[result - 1].dealDamage(100)
                        projectiles.pop(i)
                        i -= 1
                    #else:
                        #projectile.drawToScreen(screen)

            # Draws textured map
            screen.blit(map2, (0,0))
            # Draws players
            for player in players:
                player.drawToScreen(screen)
            # Draws projectiles
            for projectile in projectiles:
                projectile.drawToScreen(screen)

            if players[0].isDead and players[1].isDead:
                return run(displayInfo, (p1Score, p2Score), char1, char2, mapNum, Colors.YELLOW, Colors.YELLOW, boNum)
            elif players[0].isDead:
                char1.playDeathOn(noiseChannel)
                if p2Score + 1 < (boNum + 1) / 2:
                    return run(displayInfo, (p1Score, p2Score + 1), char1, char2, mapNum, p1BallColor, p2BallColor, boNum)
                else:
                    print('p2 won')
                    return 5

            elif players[1].isDead:
                char2.playDeathOn(noiseChannel)
                if p1Score + 1 < (boNum + 1) / 2:
                    return run(displayInfo, (p1Score + 1, p2Score), char1, char2, mapNum, p1BallColor, p2BallColor, boNum)
                else:
                    print('p1 won')
                    return 4
            # Updates screen
            frames += 1
            if frames > minFrames:
                currentPerc = min(((frames - minFrames) / maxFrames), maxPerc)
                # minX, maxX, minY, maxY = closeInMap(map1, currentPerc)
                borderInfo = closeInMap(screen, currentPerc)
                
            screen.blit(p1DispScore, (0, 0))
            screen.blit(p2DispScore, (screenW - p2DispScore.get_width(), 0))
            pygame.display.update()
            clock.tick(60)
            mouseClick = False
            # Exit code
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseClick = True
                if event.type == pygame.QUIT or pygame.key.get_pressed()[27]: # key 27 is escape
                    inGameplay = False
                    return -1

class Player():
    def __init__(self, pos, radius, sprite, lengthUnit, mapData, ballColor, num, isZaron = False, ammo = 3000):
        self.sprite = sprite
        self.pos = pos
        self.ammo = ammo
        self.overrideFrames = 0
        self.shootCooldown = 60
        self.dashCooldown = 0
        self.direction = 0
        self.dashFrames = 0
        self.lastButton = False
        self.lastTrigger = True
        self.lastDownHat = True
        self.mapData = mapData
        self.lengthUnit = lengthUnit
        self.hitbox = circleHitbox(radius)
        self.radius = radius
        self.lastAimPos = (0, 0)
        self.maxDash = 90
        self.stance = 1
        self.health = 100
        self.isDead = False
        self.ballColor = ballColor
        self.isZaron = isZaron
        self.playerNum = num
        self.immune = False
        self.dashBonus = 2.5
        # -----------------NORMALLY FALSE---------------
        self.helpToggle = True
        # ----------------------------------------------
    def update(self, buttons, aimPos, triggerValue, movePos, downHat, borderInfo):
        dashBonus = self.dashBonus
        triggerDeadzone = 0.9
        self.dashFrames = max(0, self.dashFrames - 1)
        self.dashCooldown = max(0, self.dashCooldown - 1)
        self.shootCooldown = max(0, self.shootCooldown - 1)
        self.overrideFrames = max(0, self.overrideFrames - 1)
        self.direction = math.degrees(math.atan2(aimPos[1], aimPos[0])) + 180
        if self.dashFrames < 10:
            self.immune = False
        if self.overrideFrames == 0:
            if self.dashFrames == 0:
                self.pos = move(self.pos, movePos, self.lengthUnit, self.hitbox, self.mapData)
                self.lastMovePos = movePos
            else:
                self.pos = move(self.pos, self.lastMovePos, self.lengthUnit * dashBonus, self.hitbox, self.mapData)
        else:
            self.pos = move(self.pos, self.lastMovePos, self.lengthUnit, self.hitbox, self.mapData)
        
        if not self.lastDownHat and downHat:
            self.helpToggle = not self.helpToggle
        self.lastDownHat = downHat

        if not self.lastTrigger and triggerValue > triggerDeadzone and self.dashCooldown == 0:
            self.dashFrames = 14
            self.dashCooldown = self.maxDash
            self.immune = True
        self.lastTrigger = triggerValue > triggerDeadzone

        if buttons and not self.lastButton:
            self.stance *= -1
        self.lastButton = buttons

        posX = self.pos[0]
        posY = self.pos[1]
        #if posX + self.radius < borderInfo[0] or posX - self.radius > borderInfo[1] or posY + self.radius < borderInfo[2] or posY - self.radius > borderInfo[3]:
        if posX < borderInfo[0] or posX > borderInfo[1] or posY < borderInfo[2] or posY > borderInfo[3]:
            self.dealDamage(1)
            
        if -1 * triggerValue > triggerDeadzone and self.ammo > 0 and self.shootCooldown == 0:
            self.ammo -= 1
            self.shootCooldown = 60
            webBall = Projectile(self.direction, 10, self.pos, self.radius, self.stance, self.ballColor, self.playerNum, self.isZaron)
            return webBall
        return 0

    def dealDamage (self, amount):
        self.health -= amount
        if self.health <= 0:
            self.isDead = True
        
    def drawToScreen(self, screen):
        staminaBar = pygame.Surface((self.radius * 2, rint(self.radius / 3)))
        stamPerc = self.dashCooldown / self.maxDash
        staminaBar.fill((69, 69, 42))
        if stamPerc != 0:
            staminaBar.set_colorkey((69, 69, 42))
            currentStamina = pygame.Rect(0, 0, stamPerc * self.radius * 2, rint(self.radius / 3))
            pygame.draw.rect(staminaBar, Colors.GREEN, currentStamina)
            draw(screen, staminaBar, (self.pos[0], rint(self.pos[1] - (self.radius * 1.3))))
            
        healthBar = pygame.Surface((self.radius * 2, rint(self.radius / 3)))
        healthPerc = self.health / 100
        healthBar.fill((69, 69, 42))
        if healthPerc != 1:
            healthBar.set_colorkey((69, 69, 42))
            currentHealth = pygame.Rect(0, 0, healthPerc * self.radius * 2, rint(self.radius / 3))
            pygame.draw.rect(healthBar, Colors.RED, currentHealth)
            draw(screen, healthBar, (self.pos[0], rint(self.pos[1] - (self.radius * 1.3) - rint(self.radius / 3))))
            
        if self.stance == -1:
            realImage = pygame.transform.rotate(pygame.transform.flip(self.sprite, True, False), self.direction)
        else:
            realImage = pygame.transform.rotate(self.sprite, self.direction)
        if self.dashFrames > 0:
            realImage
        draw(screen, realImage, self.pos)
        
        


class Projectile():
    def __init__(self, direction, speed, pos, playerRadius, stance, color, playerNum, isZaron = False, rad = 5):
        self.bouncesLeft = 5
        x,y = pos
        self.xSpeed = -1* speed * math.sin(math.radians(direction))
        self.ySpeed = -1 * speed * math.cos(math.radians(direction))
        angle = direction - (45 * stance)
        angle = math.radians(angle)
        x += math.sin(angle) * playerRadius * -1
        y += math.cos(angle) * playerRadius * -1
        self.pos = int(x+0.5),int(y+0.5)
        self.radius = rad
        self.hitbox = circleHitbox(self.radius)
        self.immuneFrames = 1#10
        self.xNoBounce = 0
        self.yNoBounce = 0
        self.color = color
        self.isZaron = isZaron
        self.ownerNum = playerNum
        self.speed = speed
    def changeAngle(self, direction):
        self.xSpeed = self.speed * math.cos(direction)
        self.ySpeed = self.speed * math.sin(direction)
    def fakeUpdate(self, gameMap, players):
        oldInfo = self.immuneFrames, self.xNoBounce, self.yNoBounce, self.pos, self.speed, self.xSpeed, self.ySpeed, self.bouncesLeft, self.immuneFrames, self.color
        value = self.update(gameMap, players)
        self.immuneFrames, self.xNoBounce, self.yNoBounce, self.pos, self.speed, self.xSpeed, self.ySpeed, self.bouncesLeft, self.immuneFrames, self.color = oldInfo
        return value
    def update(self, gameMap, players):
        self.immuneFrames -= 1
        self.xNoBounce -= 1
        self.yNoBounce -= 1
        posX = self.pos[0]
        posY = self.pos[1]
        strength = 5 # 0 is strongest
        if self.isZaron:
            currentDirection = math.atan2(self.ySpeed, self.xSpeed)
            if self.ownerNum == 0:
                direction = math.atan2(players[1].pos[1] - posY, players[1].pos[0] - posX)
                hasLOS = True # line of sight
                dist = math.hypot(players[1].pos[0] - posX, players[1].pos[1] - posY)
                currentXSpeed = self.xSpeed
                currentYSpeed = self.ySpeed
                self.changeAngle(direction)
                testX = int(posX + (self.xSpeed) + 0.5)
                testY = int(posY + (self.ySpeed) + 0.5)
                while dist > self.radius + players[1].radius and hasLOS:
                    testPx = gameMap.get_at((testX,testY))
                    if testPx == Colors.BLACK:
                        hasLOS = False
                    dist = math.hypot(players[1].pos[0] - testX, players[1].pos[1] - testY)
                    testX = int(testX + (self.xSpeed) + 0.5)
                    testY = int(testY + (self.ySpeed) + 0.5)
                    
                if not hasLOS:
                    # self.changeAngle(currentDirection) this works
                    self.xSpeed, self.ySpeed = currentXSpeed, currentYSpeed
                else:
                    xComp = (strength * math.cos(currentDirection)) + math.cos(direction)
                    yComp = (strength * math.sin(currentDirection)) + math.sin(direction)
                    newAngle = math.atan2(yComp, xComp)
                    # newAngle = ((strength * currentDirection) + direction) / (1+strength)
                    self.changeAngle(newAngle)
                    
            else:
                direction = math.atan2(players[0].pos[1] - posY, players[0].pos[0] - posX)
                hasLOS = True # line of sight
                dist = math.hypot(players[0].pos[0] - posX, players[0].pos[1] - posY)
                currentXSpeed = self.xSpeed
                currentYSpeed = self.ySpeed
                self.changeAngle(direction)
                testX = int(posX + (self.xSpeed) + 0.5)
                testY = int(posY + (self.ySpeed) + 0.5)
                while dist > self.radius + players[0].radius and hasLOS:
                    testPx = gameMap.get_at((testX,testY))
                    if testPx == Colors.BLACK:
                        hasLOS = False
                    dist = math.hypot(players[0].pos[0] - testX, players[0].pos[1] - testY)
                    testX = int(testX + (self.xSpeed) + 0.5)
                    testY = int(testY + (self.ySpeed) + 0.5)
                    
                if not hasLOS:
                    # self.changeAngle(currentDirection) this works
                    self.xSpeed, self.ySpeed = currentXSpeed, currentYSpeed
                else:
                    xComp = (strength * math.cos(currentDirection)) + math.cos(direction)
                    yComp = (strength * math.sin(currentDirection)) + math.sin(direction)
                    newAngle = math.atan2(yComp, xComp)
                    # newAngle = ((strength * currentDirection) + direction) / (1+strength)
                    self.changeAngle(newAngle)
                
        posX = int(posX + (self.xSpeed) + 0.5)
        posY = int(posY + (self.ySpeed) + 0.5)
        xBad = True
        testXCircle = properHitbox(self.hitbox, (posX, self.pos[1]))
        for coord in testXCircle:
            try:
                xBad = gameMap.get_at(coord) == Colors.BLACK
            except:
                xBad = True
            if xBad and self.xNoBounce < 0:
                self.xNoBounce = 1
                posX = self.pos[0]
                self.xSpeed *= -1
                self.bouncesLeft -= 1

        yBad = True
        testYCircle = properHitbox(self.hitbox, (self.pos[0], posY))
        for coord in testYCircle:
            try:
                yBad = gameMap.get_at(coord) == Colors.BLACK
            except:
                yBad = True
            if yBad and self.yNoBounce < 0:
                self.yNoBounce = 1
                posY = self.pos[1]
                self.ySpeed *= -1
                self.bouncesLeft -= 1

        if self.bouncesLeft < 1:
            return -1

        self.pos = (posX, posY)

        if self.immuneFrames < 0:
            for i in range(len(players)):
                player = players[i]
                distance = math.hypot(self.pos[0] - player.pos[0], self.pos[1] - player.pos[1])
                if distance < self.radius + player.radius:
                    if player.immune:
                        xDisp = player.pos[0] - self.pos[0]
                        yDisp = player.pos[1] - self.pos[1]
                        angle = math.atan2(yDisp, xDisp) + math.pi
                        #
                        #
                        # FIX THIS
                        self.speed *= 2
                        #
                        #
                        #
                        self.changeAngle(angle)
##                        self.xSpeed *= -2
##                        self.ySpeed *= -2
##                        self.speed *= 2
                        self.ownerNum = i
                        self.immuneFrames = 2
                        player.dashCooldown = 0
                        player.dashFrames = 0
                        # self.bouncesLeft += 5
                        self.color = Colors.LIGHTBLUE
                    elif player.isZaron:
                        result = random.randint(0, 100)
                        if result < 0: # 70
                            return -1
                        else:
                            return i+1
                    else:
                        #print('hit')
                        return i + 1

        return 0
        
    def drawToScreen(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        
class Bot():
    def __init__(self,player,enemy,mapData,num=8):
        self.player=player
        self.enemy = enemy
        self.mapData=mapData
        self.superOP = True
        self.num=num
        self.toDash = 0
    def predictBallPos(self, ball, frameCount):
        predictX = ball.pos[0] + (ball.xSpeed * frameCount)
        predictY = ball.pos[1] + (ball.ySpeed * frameCount)
        return predictX, predictY
    def update(self, Projectiles):
        self.toDash = max(0, self.toDash - 1)
        if self.superOP:
            for i in range(len(Projectiles)):
                ball = Projectiles[i]
                predictedX=self.player.pos[0]
                predictedY=self.player.pos[1]
                futureX=int(ball.xSpeed+ball.pos[0] + 0.5)
                futureY=int(ball.ySpeed+ball.pos[1] + 0.5)
                if ball.immuneFrames<=0 and ball.fakeUpdate(self.mapData, [self.player]) == 1:#(math.hypot(futureX-predictedX,futureY-predictedY))<(self.player.radius+ball.radius):  
                    if self.player.dashCooldown==0:
                        i = len(Projectiles) + 1
                        self.player.dashFrames = 14
                        self.player.dashCooldown = self.player.maxDash
                        self.player.immune = True
                        self.player.lastMovePos=(0,0)
                        #self.player.overrideFrames = 2
                        
            if False:#self.player.dashFrames == 0:
                for i in range(len(Projectiles)):
                    ball = Projectiles[i]
                    dirX=0
                    dirY=0
                    direction=self.player.lastMovePos
                    mag = math.hypot(direction[0], direction[1])
                    if mag >= 0.1:
                        if mag > 1:
                            dirX = direction[0] / mag
                            dirY = direction[1] / mag
                    else:
                        dirX = direction[0]
                        dirY = direction[1]
                    xSpeed=dirX*self.player.lengthUnit
                    ySpeed=dirY*self.player.lengthUnit

                    predictedX=self.player.pos[0]+xSpeed*self.num
                    predictedY=self.player.pos[1]+ySpeed*self.num
                    futureX=int(ball.xSpeed+ball.pos[0] + 0.5)+ball.xSpeed*(self.num-1)
                    futureY=int(ball.ySpeed+ball.pos[1] + 0.5)+ball.ySpeed*(self.num-1)
                    if (math.hypot(predictedX-futureX,predictedY-futureY))<(self.player.radius+ball.radius):                
                        angle1 = math.atan2(ball.ySpeed, ball.xSpeed)+math.pi/2
                        angle2 = math.atan2(ball.ySpeed, ball.xSpeed)-math.pi/2
                        movePos1 =(2*math.cos(angle1),2*math.sin(angle1))
                        movePos2 =(2*math.cos(angle2),2*math.sin(angle2))
                        self.player.overrideFrames=10

                        direction=movePos1
                        mag = math.hypot(direction[0], direction[1])
                        if mag >= 0.1:
                            if mag > 1:
                                dirX = direction[0] / mag
                                dirY = direction[1] / mag
                        else:
                            dirX = direction[0]
                            dirY = direction[1]
                        xSpeed=dirX*self.player.lengthUnit
                        ySpeed=dirY*self.player.lengthUnit

                        predictedX=self.player.pos[0]+xSpeed*self.num
                        predictedY=self.player.pos[1]+ySpeed*self.num
                        distance1=math.hypot(predictedX-futureX,predictedY-futureY)

                        direction = movePos2
                        mag = math.hypot(direction[0], direction[1])
                        if mag >= 0.1:
                            if mag > 1:
                                dirX = direction[0] / mag
                                dirY = direction[1] / mag
                        else:
                            dirX = direction[0]
                            dirY = direction[1]
                        xSpeed=dirX*self.player.lengthUnit
                        ySpeed=dirY*self.player.lengthUnit

                        predictedX=self.player.pos[0]+xSpeed*self.num
                        predictedY=self.player.pos[1]+ySpeed*self.num
                        distance2=math.hypot(predictedX-futureX,predictedY-futureY)
                        
                        if(distance1>distance2):
                            movePos=movePos1
                        else:
                            movePos=movePos2
                        

                        self.player.pos = move( self.player.pos, movePos,  self.player.lengthUnit,  self.player.hitbox,  self.player.mapData)
                        self.player.lastMovePos = movePos
        else:
            if self.toDash == 1 and self.player.dashCooldown == 0:
                self.player.lastMovePos = (0,0)
            elif self.player.overrideFrames <= 1 and self.player.overrideFrames != 0 and self.player.dashCooldown == 0:
                print('dodge')
                self.player.dashFrames = 14
                self.player.dashCooldown = self.player.maxDash
                self.player.immune = True
                self.player.lastMovePos=(0,0)
                self.player.overrideFrames = 0
            elif self.player.dashCooldown == 0 and self.player.overrideFrames == 0:
                reflectFrames = 12
                testNum = 1.5
                if len(Projectiles) > 0:
                    defaultBall = Projectiles[0]
                    availableDistance = self.player.radius + (self.player.lengthUnit*testNum) + defaultBall.radius
                    bestIndex = 0
                    bestFrames = 1
                    defaultX, defaultY = self.predictBallPos(defaultBall, 1)
                    bestPos = defaultX, defaultY
                    bestDistance = 1000000000000#math.hypot(self.player.pos[0] - defaultX, self.player.pos[1] - defaultY)
                    if bestDistance > availableDistance:
                        for j in range(reflectFrames):
                            for i in range(len(Projectiles)):
                                testBall = Projectiles[i]
                                if testBall.immuneFrames - j - 1<= 0:
                                    frameCount = j + 1
                                    testX, testY = self.predictBallPos(testBall, frameCount)
                                    testDistance = math.hypot(self.player.pos[0] - testX, self.player.pos[1] - testY)
                                    if testDistance < self.player.radius + (frameCount*self.player.lengthUnit*testNum) + testBall.radius and testDistance < bestDistance:
                                        bestIndex = i
                                        bestFrames = frameCount
                                        bestPos = testX, testY
                                        bestDistance = testDistance
                                        i = len(Projectiles) + 1
                                        j = reflectFrames + 1
                    if bestDistance < self.player.radius + (bestFrames*self.player.lengthUnit*testNum) + defaultBall.radius:
                        yDisp = self.enemy.pos[1] - bestPos[1]
                        xDisp = self.enemy.pos[0] - bestPos[0]
                        neededAngle = math.atan2(yDisp, xDisp)
                        neededX = bestPos[0] - (self.player.radius * math.cos(neededAngle))
                        neededY = bestPos[1] - (self.player.radius * math.sin(neededAngle))
##                        self.player.pos = (neededX, neededY)
##                        self.player.overrideFrames = bestFrames
##                        self.player.lastMovePos = (0,0)
                        neededDistance = math.hypot(neededY - self.player.pos[1], neededX - self.player.pos[0])
                        moveAngle = math.atan2(neededY - self.player.pos[1], neededX - self.player.pos[0])
                        neededFrames = int((neededDistance / self.player.lengthUnit) + 1)
                        self.player.pos = neededX, neededY
                        self.player.overrideFrames = bestFrames - 2
                        
##                        self.player.movePos = (0,0)
##                        self.player.lastMovePos = (0,0)
##                        bestBall = Projectiles[bestIndex]
##                        bestBall.pos = (int(bestPos[0] + 0.5), int(bestPos[1] + 0.5))
##                        bestBall.changeAngle(neededAngle)
##                        bestBall.immuneFrames = 2
                        
##                        self.player.overrideFrames = bestFrames
##                        if neededFrames > reflectFrames:
##                            #print('houston we have a problem, ' + str(neededFrames) + ' versus ' + str(reflectFrames))
##                            test = 3
####                            self.player.overrideFrames = neededFrames
####                            self.player.movePos = (5*math.cos(moveAngle), 5*math.sin(moveAngle))
####                            self.player.lastMovePos = (5*math.cos(moveAngle), 5*math.sin(moveAngle))
##                        if neededFrames > bestFrames:
##                            #print('beep boop')
##                            test= 5
##                        else:
##                            #print('moved')
##                            self.player.overrideFrames = bestFrames + 1
##                            self.toDash = bestFrames - neededFrames + 1
##                            self.player.movePos = (5*math.cos(moveAngle), 5*math.sin(moveAngle))
##                            self.player.lastMovePos = (5*math.cos(moveAngle), 5*math.sin(moveAngle))
                        
                    
