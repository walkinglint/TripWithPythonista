from scene import *
from random import random, randrange, uniform
import colorsys
from math import cos, pi, sin
from noise import PerlinNoise
import numpy as np
circles = []
clss = []
cn = 0
nc = 1
nel = 100
elidx = 0
nl = []
def mp(v, ol, oh, nl, nh):
	return nl + (v - ol) * (nh - nl)/(oh - ol)
class Circle():
	def __init__(self, hue, parent):
		self.color = colorsys.hsv_to_rgb(hue, 1, 1)
		self.parent = parent
		circles.append(self)
	def set_location(self, loc):
		self.loc = loc
	def set_r(self, r):
		self.r = r
	def draw(self):
		push_matrix()
		translate(self.parent.loc.x, self.parent.loc.y)
		translate(self.loc.x, self.loc.y)
		stroke(*self.color)
		stroke_weight(1)
		no_fill()
		ellipse(-self.r, -self.r, 2 * self.r, 2 * self.r)
		pop_matrix()
class Circles():
	def __init__(self, depth, loc, n, clsr, r, hue, da, ira, dra, icra, dcra):
		global elidx
		self.loc = loc
		self.n = n
		self.clsr = clsr
		self.r = r
		self.hue = hue
		self.da = da
		self.dra = dra
		self.dcra = dcra
		self.a = 0
		self.ra = ira
		self.cra = icra
		self.cls = []
		self.clss = []
		r1 = randrange(3, 20)
		r2 = randrange(2, 500)
		r3 = randrange(50, 300)
		elidx += 1
		if nel <=elidx:
			elidx = 0
			init_pn()
		r4 = nl[elidx]
		elidx += 1
		r5 = uniform(-1, 1) / 15
		r6 = uniform(0, 2 * pi)
		r7 = uniform(-1, 1) / 30
		r8 = uniform(0, 2 * pi)
		r9 = uniform(-1, 1) / 30
		for i in range(n):
			if 0 < depth:
				a = 2 * pi * i / n
				r = 200
				p = Point(r * cos(a), r * sin(a))
				clss.append(Circles(depth - 1, p, r1, r2, r3, r4, r5, r6, r7, r8, r9))
			self.cls.append(Circle(self.hue, self))
	def set_location(self, loc):
		self.loc = loc
	def update(self):
		for i in range(self.n):
			c = self.cls[i]
			a = 2 * pi * i / self.n + self.a
			r = self.clsr * (1 + cos(self.ra)) / 2
			c.set_location(Point(r * cos(a), r * sin(a)))
			cr = self.r * (2 + cos(self.cra)) / 2
			c.set_r(cr)
		self.a += self.da
		self.ra += self.dra
		self.cra += self.dcra
def init_pn():
	global nl
	pn = PerlinNoise(size = (1, nel))
	l = pn.getData([1, nel])
	l2 = [abs(int(l[i])) for i in range(len(l))]
	mx = max(l2)
	mn = min(l2)
	nl = [mp(l2[i], mn, mx, 0, 1) for i in range(len(l2))]
class MyScene(Scene):
	def setup(self):
		background('black')
		init_pn()
		self.init()
	def init(self):
		global circles
		global clss 
		global cn
		global elidx
		cn = 0
		circles = []
		clss = []
		for i in range(nc):
			elidx += 1
			if nel <=elidx:
				elidx = 0
				init_pn()
			clss.append(Circles(1, Point(0, 0), randrange(3, 20), randrange(2, 500), randrange(50, 300), nl[elidx], uniform(-1, 1) / 15, uniform(0, 2 * pi), uniform(-1, 1) / 30, uniform(0, 2 * pi), uniform(-1, 1) / 30))
	def update(self):
		global cn
		cn += 1
		if cn % 40 == 0:
			self.init()
		translate(int(self.size.w // 2), int(self.size.h // 2))
		for cls in clss:
			cls.update()
		for c in circles:
			c.draw()
	def touch_began(self, touch):
		self.init()
if __name__ == '__main__':
	run(MyScene(), PORTRAIT, 2)

