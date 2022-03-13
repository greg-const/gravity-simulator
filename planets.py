from vec2d import vec2d as vec
from helpfulfunctions import constrain
from random import randint


class Particle:

    def __init__(self, x, y):
        self.pos = vec(x, y)
        self.prev = vec(x, y)
        self.initialvel = vec(0, 0)
        self.vel = self.initialvel

        self.acc = vec(0, 0)
        self.col = (21, 21, 21)

    def update(self):
        self.acc = self.acc.limit(8)
        self.vel = self.vel.add(self.acc)
        self.vel = self.vel.limit(30)
        self.pos = (self.pos.add(self.vel))  # .add(self.acc.scale(.5*0.00027777777))
        self.acc = vec(0, 0)

    def attracted(self, target):
        force = target.sub(self.pos)
        d = force.mag()
        G = 10000
        d = constrain(d, 20, 10000)
        strength = G / (d*d)
        force = force.setmag(strength)

        self.acc = self.acc.add(force)

    def newcol(self, col):
        self.col = col

    def randvel(self):
        return randint(-10, 10)