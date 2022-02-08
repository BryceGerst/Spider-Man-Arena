
import pygame, Colors, Scaler

def loadMap1(screenDimensions):
    width = screenDimensions[0]
    height = screenDimensions[1]
    background = pygame.image.load('Images/framed2.png')
    background = pygame.transform.scale(background, (width, height))
    textured = pygame.image.load('Images/framed2.png')
    textured = pygame.transform.scale(textured, (width, height))
    
    return background, textured

def loadMap2(screenDimensions):
    width = screenDimensions[0]
    height = screenDimensions[1]
    background = pygame.image.load('Images/Snoim.png')
    background = pygame.transform.scale(background, (width, height))
    textured = pygame.image.load('Images/SnoimTextured.png')
    textured = pygame.transform.scale(textured, (width, height))
    
    return background, textured

def loadMap3(screenDimensions):
    width = screenDimensions[0]
    height = screenDimensions[1]
    background = pygame.image.load('Images/TheTrench.png')
    background = pygame.transform.scale(background, (width, height))
    textured = pygame.image.load('Images/TheTrenchTextured.png')
    textured = pygame.transform.scale(textured, (width, height))
    
    return background, textured

def loadMap4(screenDimensions):
    width = screenDimensions[0]
    height = screenDimensions[1]
    background = pygame.image.load('Images/==.png')
    background = pygame.transform.scale(background, (width, height))
    textured = pygame.image.load('Images/==Textured.png')
    textured = pygame.transform.scale(textured, (width, height))
    
    return background, textured

def loadMap5(screenDimensions):
    width = screenDimensions[0]
    height = screenDimensions[1]
    background = pygame.image.load('Images/Technical.png')
    background = pygame.transform.scale(background, (width, height))
    textured = background#pygame.image.load('Images/TechnicalTextured.png')
    textured = pygame.transform.scale(textured, (width, height))
    
    return background, textured

def loadSoccer(screenDimensions):
    width = screenDimensions[0]
    height = screenDimensions[1]
    background = pygame.image.load('Images/Soccer.png')
    background = pygame.transform.scale(background, (width, height))
    
    return background

def loadEmptyMap(screenDimensions):
    width = screenDimensions[0]
    height = screenDimensions[1]
    background = pygame.image.load('Images/FinalArena.png')
    background = pygame.transform.scale(background, (width, height))
    
    return background


    
