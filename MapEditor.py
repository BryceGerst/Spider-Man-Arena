import pygame, sys, StartUp, Maps
pygame.init()

screen, clock = StartUp.start()
screenW, screenH, fps = StartUp.giveDisplayInfo()

editting = True
blankMap = Maps.loadEmptyMap((screenW, screenH))

while editting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[27]: # key 27 is escape
            editting = False
    screen.blit(blankMap, (0,0))
    pygame.display.update()

pygame.quit()
sys.exit()
