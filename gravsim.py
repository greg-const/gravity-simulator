import pygame as pg
import pygame.gfxdraw
from planets import Particle as particle
from random import randint
from vec2d import vec2d as vec
from subprocess import Popen
from math import sin as sin
from math import cos as cos


class Game:
    def __init__(self):
        pg.init()
        # -- vars --
        self.disp_h = 1000
        self.disp_w = 1850
        self.fps = 60
        self.initialv = vec(0, 0)
        self.t = 255

        self.initialparticles = 0
        self.ltoggle = 1

        # for lemniscate testing
        self.mag = 6.25
        self.ang = 120
        # --

        self.radius = 10
        self.linethickness = 14

        self.wincommunication = 0

        self.colorassimilation = 0

        self.surface = pg.display.set_mode((self.disp_w, self.disp_h))  # , pg.FULLSCREEN)
        self.pos = (0, 0)
        self.clock = pg.time.Clock()
        self.s = pg.Surface((self.disp_w, self.disp_h), pg.SRCALPHA, 32)

        self.universepic = pg.image.load('universe.jpg')
        self.universe = pg.Surface((self.disp_w, self.disp_h), pg.SRCALPHA, 32)
        self.universe.blit(self.universepic, (0, 0))
        if self.wincommunication:
            Popen("python paramset.py")
        self.windowname = pg.display.set_caption("Gravity Sim")
        self.attractors = [vec(self.disp_w * 0.25, self.disp_h/2), vec(self.disp_w * 0.75, self.disp_h/2)]
        self.particles = []
        # ----------

        self.loop()

    def loop(self):
        currentpos = (0, 0)
        speed = vec(0, 0)
        while True:
            self.clock.tick(self.fps)
            self.pos = pg.mouse.get_pos()

            self.surface.fill((50, 50, 50))
            #self.surface.blit(self.universepic, (0, 0))
            self.events()

            if len(self.particles) < self.initialparticles:
                self.particles.append(particle(randint(1, self.disp_w), randint(1, self.disp_h)))

            for p in self.particles:
                if self.bounds(p.pos.x, p.pos.y):
                    for j in self.attractors:
                        p.attracted(j)
                    if self.colorassimilation:
                        try:
                            p.newcol(self.universepic.get_at((int(p.pos.x), int(p.pos.y))))
                        except IndexError:
                            pass
                    p.update()
                    self.showparticle(p)

            i = 0
            while i < len(self.attractors):
                pos = (int(self.attractors[i].x), int(self.attractors[i].y))
                if self.colorassimilation:
                    try:
                        inverse = self.universe.get_at(pos)
                        color = (255 - inverse[0], 255 - inverse[1], 255 - inverse[3])
                    except IndexError:
                        color = (0, 0, 0)
                else:
                    color = (100, 255, 100)
                pg.draw.circle(self.surface,
                               color,
                               pos,
                               10)
                i += 1

            self.surface.blit(self.s, (0, 0))

            if self.wincommunication:
                f = open("line.txt", "r")
                lines = f.readlines()
                if len(lines) > 0:
                    self.ltoggle = self.setl(lines[0], self.ltoggle)
                    self.initialv = vec(float(lines[1]), float(lines[2]))
                    if int(lines[3]):
                        self.clear()
                f.close()
            else:

                lastpos = currentpos
                currentpos = self.pos
                lastspeed = speed
                speed = self.getcursorspeed(lastpos, currentpos).scale(-.25)
                self.initialv = speed
                #self.showinitialv(speed, lastspeed)

            pg.display.update()

    def bounds(self, x, y):
        point = pg.Rect(x, y, 1, 1)
        screen = pg.Rect(0, 0, self.disp_w, self.disp_h)
        return pg.Rect.colliderect(point, screen)

    def showinitialv(self, speed, lastspeed):
        x, y = self.pos[0], self.pos[1]

        lastvector = vec(int(x + 8 * lastspeed.x), int(y + 8 * lastspeed.y))
        vector = vec(int(x + 8 * speed.x), int(y + 8 * speed.y))
        if vector.mag()-1 > lastvector.mag():
            vector = vector.setmag(vector.mag()+100)
            vector.x = int(vector.x)
            vector.y = int(vector.y)
        elif vector.mag()+1 < lastvector.mag():
            vector = vector.setmag(vector.mag() - 100)
            vector.x = int(vector.x)
            vector.y = int(vector.y)
        else:
            vector = vec(int(x + 8 * speed.x), int(y + 8 * speed.y))
        pg.draw.line(self.surface, (255, 100, 100), (vector.x, vector.y), (x, y), )
        pg.gfxdraw.circle(self.surface, vector.x, vector.y, 3, (255, 100, 100))
        pg.gfxdraw.filled_circle(self.surface, vector.x, vector.y, 3, (255, 100, 100))
        pg.gfxdraw.circle(self.surface, x, y, 3, (255, 100, 100))
        pg.gfxdraw.filled_circle(self.surface, x, y, 3, (255, 100, 100))

    def getcursorspeed(self, old, new):
        old = vec(old[0], old[1])
        new = vec(new[0], new[1])
        return old.sub(new)

    def clear(self):
        self.surface.fill((41, 41, 41))
        self.s = pg.Surface((self.disp_w, self.disp_h), pg.SRCALPHA, 32)
        # self.attractors = []
        self.particles = []

    def setl(self, line, f):
        if line == "1":
            return 1
        elif line == "0":
            return 0
        else:
            return f

    def showparticle(self, p):
        if self.ltoggle:
            pg.draw.line(self.s, (p.col[0], p.col[1], p.col[2]), (p.prev.x, p.prev.y), (p.pos.x, p.pos.y), 8)
            pg.gfxdraw.aacircle(self.surface, int(p.pos.x), int(p.pos.y), self.radius, (p.col[0], p.col[1], p.col[2]))
            pg.gfxdraw.filled_circle(self.surface, int(p.pos.x), int(p.pos.y), self.radius, (p.col[0], p.col[1], p.col[2]))

        else:
            pg.gfxdraw.aacircle(self.surface, int(p.pos.x), int(p.pos.y), self.radius, (p.col[0], p.col[1], p.col[2]))
            pg.gfxdraw.filled_circle(self.surface, int(p.pos.x), int(p.pos.y), self.radius, (p.col[0], p.col[1], p.col[2]))
        p.prev.x = p.pos.x
        p.prev.y = p.pos.y

    def newparticle(self, x, y, col, vel):
        p = particle(x, y)
        if col == 0:
            p.newcol((randint(0, 255),
                      randint(0, 255),
                      randint(0, 255)))
        else:
            p.col = col
        p.vel = vel
        self.particles.append(p)

    def events(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                quit()
            keys = pg.key.get_pressed()
            if keys[pg.K_p]:
                p = self.pos
                col = (randint(0, 255), randint(0, 255), randint(0, 255))

                self.newparticle(p[0], p[1], col, self.initialv)
                # self.clock.tick(8)
            if keys[pg.K_c]:
                self.clear()

            if keys[pg.K_a]:
                self.attractors = []

            if keys[pg.K_s]:
                self.colorassimilation = not self.colorassimilation

            if keys[pg.K_l]:
                if self.ltoggle:
                    self.ltoggle = 0
                    self.s = pg.Surface((self.disp_w, self.disp_h), pg.SRCALPHA, 32)
                    self.clock.tick(10)
                else:
                    self.s = pg.Surface((self.disp_w, self.disp_h), pg.SRCALPHA, 32)
                    self.ltoggle = 1
                    self.clock.tick(10)

            if keys[pg.K_t]:
                self.t -= 20
                if self.t <= 0:
                    self.t = 255

            if keys[pg.K_x]:
                pg.quit()
                quit()

            if keys[pg.K_i]:
                self.mag += 0.01
                vel = vec(self.mag * sin(self.ang), self.mag * cos(self.ang)).scale(-1)
                self.newparticle(self.disp_w/2, self.disp_h/2, 0, vel)
                print(self.mag)

            if pg.mouse.get_pressed() == (1, 0, 0):
                p = self.pos
                self.attractors.append(vec(p[0], p[1]))
                self.clock.tick(8)


# ---------------------------------------------------------------

game = Game()
