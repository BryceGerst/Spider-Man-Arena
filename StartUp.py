# This is the initialization file
# The main purpose to obtain and deliver system information, as well as to actually open the game window

import ctypes, pygame, time, sys
# The following retrieves display information
user32 = ctypes.windll.user32
screenW, screenH = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# screenW, screenH = 96, 54
fps = 60

def giveDisplayInfo():
    return screenW, screenH, fps

def start():
    screen = pygame.display.set_mode([screenW, screenH], pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    return screen, clock
