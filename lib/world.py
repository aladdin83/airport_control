import pygame, random
from pygame.locals import *
from random import *
import configparser
import os

from utils import *
from camera import *
from globals import *
from plane import *
from airport import *

class World(object):
	def __init__(self, scene_name, screen):
		self.screen = screen
		config = configparser.ConfigParser()

		self.elements = []
		self.airports = []
		self.setup_elements()
		self.collidelist = []
		#scene setup

		config.read(os.path.join(ROOT_PATH,'data','scenes',scene_name,'scene.ini'))
		self.sky, self.sky_rect = load_image(config.get('background','sky_image'))
		self.sky_rect = Rect(config.getint('background','sky_x'), config.getint('background','sky_y'),config.getint('background', 'sky_width'), config.getint('background', 'sky_height'))
		self.width , self.height = config.getint('scene','width'), config.getint('scene','height')
		self.shadow_offset = config.getint('scene','shadow_offset_x'), config.getint('scene','shadow_offset_y')

		self.x = 0

	def setup_elements(self):
		port = Airport(Rect(730,600,30,30),[(740,615),(0,160)])
		self.airports.append(port)
		port = Airport(Rect(200,110,30,30),[(215,120),(10,0)])
		self.airports.append(port)

	def sendNewPlane(self):
		plane = plane = Plane('airbus',self.random_entering_point(), 0.5, len(self.elements),self)
		self.elements.append(plane)

	def random_entering_point(self):
		i = random.randint(0,3)
		if i == 0:
			x = self.screen.get_width() + 50
			y = randint(0,self.screen.get_height())
		elif i == 1:
			x = randint(0,self.screen.get_width())
			y = self.screen.get_height() + 50
		elif i == 2:
			x = -50
			y = random.randint(0,self.screen.get_height())
		elif i == 3:
			x = random.randint(0,self.screen.get_width())
			y = -50
		return x, y
	def is_mouse_free(self, id):
		for e in self.elements:
			if e.released == False and not e.id == id:
				return False
		return True
	def update(self):
		for e in self.elements:
			for a in self.airports:
				if a.check_plane_collide(e) and e.landing == False:
					e.landing = True
					e.set_landing_path(a.get_landing_path())
			e.update()
		self.check_collision()

	def check_collision(self):
		rects = []
		self.collidelist = []
		for e in self.elements:
			rects.append(Rect(e.x,e.y,e.width,e.height))
		if len(rects) > 1:
			for r in rects:
				collides = r.collidelistall(rects)
				if len(collides) > 1:
					self.collidelist.append(collides)

	def check_point_for_airports(self, point):
		for a in self.airports:
			if a.rect.collidepoint(point):
				return a.get_landing_path()[0] , True, True
		return point , False, False
	def draw(self, screen):
		screen.fill(self.sky.get_at((5,0)))
		screen.blit(self.sky, (0,0), self.sky_rect)
		#draw elements
		for e in self.elements:
			if not e.dirty:
				e.draw(screen)
		if len(self.collidelist) > 1:
				for c in self.collidelist:
					for ce in c:
						rect = self.elements[ce].get_rect()
						pygame.draw.rect(screen,(255,0,0),rect,2)
					#pygame.draw.rect(screen,(255,0,0),c,2)
