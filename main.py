# File: main.py
# Name: Andrew Holbrook
# Date: 11/30/2013

import pygame
import time
from etgg1801util import Vector2
from GameObjects import *

WIN_WIDTH = 800
WIN_HEIGHT = 600

pygame.init()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
backSurface = win.copy()

clock = pygame.time.Clock()
done = False

keyPressed = []

bgLayer1 = pygame.image.load('background.png').convert_alpha()
bgLayer2 = pygame.image.load('background2.png').convert_alpha()

glass = Glass()

portal = Portal(WIN_WIDTH // 2, WIN_HEIGHT // 2, 50)
portal.glass = glass
ship = Ship()

while not done:
    evtList = pygame.event.get()
    for evt in evtList:
        if evt.type == pygame.QUIT:
            done = True
        elif evt.type == pygame.KEYDOWN:
            keyPressed.append(evt.key)
        elif evt.type == pygame.KEYUP:
            keyPressed.remove(evt.key)
    
    dtime = clock.tick_busy_loop(60)

    if pygame.K_LEFT in keyPressed:
        ship.rotateCW(dtime)
    if pygame.K_RIGHT in keyPressed:
        ship.rotateCCW(dtime)
    if pygame.K_SPACE in keyPressed:
        ship.fire()
    
    glass.update(dtime)
    portal.update(dtime)
    ship.update(dtime)

    portalToShip(portal, ship)
    
    backSurface.blit(bgLayer1, (0, 0))
    portal.render(backSurface)
    ship.render(backSurface)
    glass.render(backSurface)

    
    
    backSurface.blit(bgLayer2, (0, 0))
    win.blit(backSurface, (glass.win_x, 0))
    
    
    pygame.display.flip()

# display "Game Over" screen
glass.showGameOver(win)
win.blit(bgLayer2, (0, 0))

pygame.display.flip()

time.sleep(5)
pygame.quit()

