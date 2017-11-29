# File: GameObjects.py
# Name: Andrew Holbrook
# Date: 11/30/2013

import pygame
import math
from random import randint
from etgg1801util import *

class Ship(object):
    def __init__(self, angle=0, rotateRate=360.0/1500.0, MAX_BULLETS=3):
        self.angle = angle
        self.rotateRate = rotateRate
        self.MAX_BULLETS = MAX_BULLETS
        self.image = pygame.image.load('ship.png').convert_alpha()
        
        self.bulletList = []
        
    def rotateCW(self, dtime):
        self.angle -= self.rotateRate * dtime
        if self.angle < 0:
            self.angle += 360
    
    def rotateCCW(self, dtime):
        self.angle += self.rotateRate * dtime
        if self.angle >= 360:
            self.angle -= 360
    
    def fire(self):
        if len(self.bulletList) == 3:
            return
        
        b = Bullet(self.angle)
        self.bulletList.append(b)
    
    def update(self, dtime):
        for b in self.bulletList:
            b.update(dtime)
            if b.depth >= 250:
                self.bulletList.remove(b)
    
    def render(self, surface):
        x = 400 + 250 * math.cos(math.radians(self.angle))
        y = 300 - 250 * math.sin(math.radians(self.angle))
        
        tmpImg = pygame.transform.rotate(self.image, self.angle)
        
        x -= tmpImg.get_width() // 2
        y -= tmpImg.get_height() // 2
        
        surface.blit(tmpImg, (x, y))
        
        for b in self.bulletList:
            b.render(surface)

class Bullet(object):
    def __init__(self, angle, VEL_MAG=250.0/1500.0):
        self.angle = angle
        self.depth = 0
        self.radius = 8
        self.VEL_MAG = VEL_MAG
        
        self.bx = 0
        self.by = 0
        self.br = 0
    
    def update(self, dtime):
        self.depth += self.VEL_MAG * dtime
    
    def render(self, surface):
        if self.depth >= 250:
            return
        
        self.br = (1.0 - (self.depth / 250.0)) * self.radius
        self.bx = 400 + (250 - self.depth) * math.cos(math.radians(self.angle))
        self.by = 300 - (250 - self.depth) * math.sin(math.radians(self.angle))
        
        pygame.draw.circle(surface, (255,0,0), (int(self.bx), int(self.by)), int(self.br))

class Portal(object):
    def __init__(self, x, y, radius, COLOR_UPDATE_DELAY=100.0):
        self.pos = Vector2(x, y)
        self.radius = radius
        self.color = [0, 0, 0]
        self.COLOR_UPDATE_DELAY = COLOR_UPDATE_DELAY
        self.curColorUpdateDelay = COLOR_UPDATE_DELAY
        
        self.asteroidList = []
        self.emitDelay = randint(500, 1000)
    
    def emitAsteroid(self):
        self.asteroidList.append(Asteroid())
    
    def update(self, dtime):
        self.curColorUpdateDelay -= dtime
        while self.curColorUpdateDelay <= 0:
            self.curColorUpdateDelay += self.COLOR_UPDATE_DELAY
            self.color[0] = randint(0, 255)
            self.color[1] = randint(0, 255)
            self.color[2] = randint(0, 255)
        
        for a in self.asteroidList:
            a.update(dtime)
            if a.depth <= -50:
                self.asteroidList.remove(a)
                self.glass.addBreak((a.bx, a.by), a.VEL_MAG)
        
        self.emitDelay -= dtime
        if self.emitDelay <= 0:
            self.emitDelay = randint(500, 1500)
            self.emitAsteroid()
    
    def render(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), self.pos.getPos(), self.radius)
        pygame.draw.circle(surface, self.color, self.pos.getPos(), self.radius,\
                           2)
        
        for a in self.asteroidList:
            a.render(surface)

class Asteroid(object):
    image = None
    
    def __init__(self):
        if Asteroid.image == None:
            Asteroid.image = pygame.image.load('asteroid.png').convert_alpha()
        
        self.angle = randint(0, 359)
        self.depth = 250
        self.VEL_MAG = -randint(25, 200) / 1500.0
        self.rotAngle = 0
        self.rotRate = 360.0 / randint(500, 5000)
        if randint(0, 1):
            self.rotRate *= -1
        
        self.bx = 0
        self.by = 0
        self.br = 50
    
    def update(self, dtime):
        self.rotAngle += self.rotRate * dtime
        if self.rotAngle >= 360:
            self.rotAngle -= 360
        elif self.rotAngle < 0:
            self.rotAngle += 360
        
        self.depth += self.VEL_MAG * dtime
    
    def render(self, surface):
        tmpImg = pygame.transform.rotate(Asteroid.image, self.rotAngle)
        x = 400 + (250 - self.depth) * math.cos(math.radians(self.angle))
        y = 300 - (250 - self.depth) * math.sin(math.radians(self.angle))
        
        scale = 1.0 - (self.depth / 250.0)
        
        w = int(tmpImg.get_width() * scale)
        h = int(tmpImg.get_height() * scale)
        
        self.bx = x
        self.by = y
        
        x -= w // 2
        y -= h // 2
        
        tmpImg = pygame.transform.scale(tmpImg, (w, h))
        
        surface.blit(tmpImg, (x, y))
        
        self.br = 50 * scale

class Material(object):
    def __init__(self):
        pass
    
    def update(self, dtime):
        pass
    
    def render(self, surface):
        pass

class Glass(object):
    def __init__(self, numImages=10):
        self.imgList = []
        for i in range(0, numImages):
            tmpImg = pygame.image.load('glass' + str(i) + '.png').convert_alpha()
            self.imgList.append(tmpImg)
        
        self.breakList = []
        
        self.win_state = 'IDLE'
        self.win_x = 0
        self.win_vx = -100.0 / 50.0
        self.win_ax = 2.0 / 1000.0
        
        self.font = pygame.font.Font('kongtext.ttf', 50)
    
    def addBreak(self, pos, vel_mag):
        scale = -vel_mag / (70.0 / 1500.0)
        tmpImg = self.imgList[randint(0, 9)]
        tmpImg = pygame.transform.rotate(tmpImg, randint(0, 359))
        
        w = int(tmpImg.get_width() * scale)
        h = int(tmpImg.get_height() * scale)
        tmpImg = pygame.transform.scale(tmpImg, (w, h))
        
        self.breakList.append((pos[0], pos[1], tmpImg))
        
        self.win_state = 'SHAKING'
        self.win_vx = -100.0 / 50.0
    
    def getNumBreaks(self):
        return len(self.breakList)
    
    def showGameOver(self, surface):
        surface.fill((255, 0, 0))
        fontSurface = self.font.render('Game Over', True, (0, 0, 0))
        
        fontX = 400 - fontSurface.get_width() // 2
        fontY = 300 - fontSurface.get_height() // 2
        surface.blit(fontSurface, (fontX, fontY))
    
    def update(self, dtime):
        if self.win_state == 'SHAKING':
            self.win_x += self.win_vx * dtime
            if self.win_x <= -50:
                self.win_x = -50 + (-50 - self.win_x)
                self.win_vx = -self.win_vx
            elif self.win_x >= 50:
                self.win_x = 50 - (self.win_x - 50)
                self.win_vx = -self.win_vx
            
            if self.win_vx < 0:
                self.win_vx += self.win_ax * dtime
            elif self.win_vx > 0:
                self.win_vx -= self.win_ax * dtime
            
            if abs(self.win_vx) <= 0.25:
                self.win_x = 0
                self.win_vx = -100.0 / 50.0
                self.win_state = 'IDLE'
    
    def render(self, surface):
        for b in self.breakList:
            x = b[0] - b[2].get_width() // 2
            y = b[1] - b[2].get_height() // 2
            surface.blit(b[2], (x, y))

def portalToShip(portal, ship):
    for b in ship.bulletList:
        for a in portal.asteroidList:
            if a.depth <= 0:
                continue
            
            if bulletToAsteroid(b, a):
                portal.asteroidList.remove(a)
                ship.bulletList.remove(b)
                break

def bulletToAsteroid(bullet, asteroid):
    dist = (bullet.bx - asteroid.bx) ** 2 + (bullet.by - asteroid.by) ** 2
    dist **= 0.5
    
    if dist <= bullet.br + asteroid.br:
        return True
    
    return False

