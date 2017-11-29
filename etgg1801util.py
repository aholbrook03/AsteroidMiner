# File: etgg1801util.py
# Name: Andrew Holbrook
# Date: 11/30/2013

from math import sin, cos, radians

class Vector2(object):  
    @staticmethod
    def copyFromVector(v):
        return Vector2(v.x, v.y)

    @staticmethod
    def initFromPolar(mag, angle):
        return Vector2(mag * cos(radians(angle)), mag * -sin(radians(angle)))
    
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
    
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    
    def getPos(self):
        return (int(self.x), int(self.y))
    
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def normalize(self):
        tmpLen = self.length()
        if tmpLen != 0:
            self.x /= tmpLen
            self.y /= tmpLen
    
    # scalar operations
    def addScalar(self, s):
        self.x += s
        self.y += s
    
    def subScalar(self, s):
        self.x -= s
        self.y -= s
    
    def mulScalar(self, s):
        self.x *= s
        self.y *= s
    
    def divScalar(self, s):
        self.x /= s
        self.y /= s
    
    # vector operations
    def addVector(self, v):
        self.x += v.x
        self.y += v.y
    
    def subVector(self, v):
        self.x -= v.x
        self.y -= v.y
    
    # other operations
    def distance(self, other):
        tmpVector = Vector2.copyFromVector(self)
        tmpVector.subVector(other)
        
        return tmpVector.length()

Vector2.ZERO = Vector2()

class BoundingCircle(object):
    def __init__(self, x, y, radius):
        self.pos = Vector2(x, y)
        self.radius = radius
    
    def isCollision(self, other):
        dist = self.pos.distance(other)
        if dist <= self.radius + other.radius:
            return True
        
        return False

