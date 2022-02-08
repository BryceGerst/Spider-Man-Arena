# This is the image loading file
# The images need to be loaded somewhere, so it is best to do it all in one place

import pygame
# The following method is to make adding images faster, as it uses fewer characters
def find(fileName): # The fileName parameter should include .png, .jpg, etc.
    return pygame.image.load('Images/' + fileName)

# --------------------------
# Image loading section
spiderman = find('Spider-Sprite.png')
peter = find('Peter.png')
ironman = find('Ironman.png')
poggle = find('Poggle.png')
greengoblin = find('GreenGoblin.png')
lemon = find('JohnLemon.png')
nut = find('BabyNut.png')
chrome = find('Chrome.png')
flap = find('FlappyBird.png')
donatello = find('Donatello.png')
hcpss = find('HCPSS.png')
washMon = find('WashingtonMonument.png')


r2 = find('R2D2.png')
p1win = find('p1wins.png')
p2win = find('p2wins.png')

# --------------------------
