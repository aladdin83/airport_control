import random
import math
import pygame.gfxdraw

from element import *

class Plane(Element):
	def __init__(self, name ,startpos, speed, id, world):
		Element.__init__(self, name)
		self.id = id
		self.x, self.y = startpos
		self.angle = 0
		self.speed = speed
		self.track = []
		self.released = True
		self.draw_angle = 0
		self.target = self.get_random_target()
		self.landing = False
		self.landing_size = (self.width / 2 , self.height / 2)
		self.dirty = False
		self.world = world
		self.connected = False
		self.newTrack = False
	def get_rect(self):
		return pygame.Rect(self.x, self.y, self.width, self.height)
	def get_random_target(self):
		screen = pygame.display.get_surface()
		x = random.randint(0,screen.get_width())
		y = random.randint(0,screen.get_height())
		side = random.randint(0,3)
		if side == 0:
			target = (screen.get_width() - self.width ,y)
		elif side == 1:
			target = (0 + self.width ,y)
		elif side == 2:
			target = (x, screen.get_height() - self.height)
		elif side == 3:
			target = (x, 0 + self.height)
		return target
	def update(self):
		if len(self.track):
			next_point = self.track[0]
			while self.is_point_inside(next_point):
				if self.released or not self.is_mouse_over():
					self.track.pop(0)
					if len(self.track):
						next_point = self.track[0]
					else: break
				else:
					break
		else:
			if self.landing:
				self.dirty = True
			elif self.is_point_inside(self.target):
				self.target = self.get_random_target()
			next_point = self.target
		center = self.center()	
		diffx = abs(next_point[0] - center['x'])
		diffy = abs(next_point[1] - center['y'])
		hyp = math.hypot(diffx, diffy)

		#update angle:
		next_poing_angle = 0
		if next_point[0] > center['x'] and next_point[1] > center['y']:
			next_point_angle = 90 - math.degrees(math.asin(diffy/hyp))
		elif next_point[0] < center['x'] and next_point[1] > center['y']:
			next_point_angle = math.degrees(math.asin(diffy/hyp)) + 270
		elif next_point[0] < center['x'] and next_point[1] < center['y']:
			next_point_angle = 270 - math.degrees(math.asin(diffy/hyp)) 
		elif next_point[0] > center['x'] and next_point[1] < center['y']:
			next_point_angle = math.degrees(math.asin(diffy/hyp)) + 90
		self.angle = next_point_angle
			
		if self.landing:
			self.draw_angle = self.angle
		else:
			if abs(self.draw_angle - self.angle) <= self.speed:
				self.draw_angle = self.angle
			elif abs(self.draw_angle - self.angle) > 180:
				if self.draw_angle < self.angle:
					self.draw_angle -= self.speed
					if self.draw_angle < 0:
						self.draw_angle += 360
				else:
					self.draw_angle += 1
					if self.draw_angle > 360:
						self.draw_angle -= 360
			elif self.draw_angle < self.angle:
				self.draw_angle += self.speed
			elif self.draw_angle > self.angle:
				self.draw_angle -= self.speed
		if self.newTrack:
			self.draw_angle = self.angle
			self.newTrack = False
		
		self.vector = {"y":(self.speed * (diffy / hyp)), "x": (self.speed * (diffx / hyp))}
		
		#print next_point_angle
		if next_point[0] < center['x']:
			x = center['x'] - self.vector['x']
		else:
			x = center['x'] + self.vector['x']
		if next_point[1] < center['y']:
			y = center['y'] - self.vector['y']
		else:
			y = center['y'] + self.vector['y']

		self.set_center({'x': x, 'y': y})
		
		#update Mouse Event
		if self.landing:
			if self.landing_size[0] < self.width:
				self.width -= 1
			if self.landing_size[1] < self.height:
				self.height -= 1
		elif self.world.is_mouse_free(self.id):
			self.check_mouse_event()
	def check_mouse_event(self):
		mouse_state = pygame.mouse.get_pressed()
		if mouse_state[0]:
			if self.released and self.is_mouse_over():
				self.track = []
				self.released = False
				self.newTrack = True
			pos = pygame.mouse.get_pos()
			if not self.released:
				if len(self.track): 
					distance = abs(self.track[-1][0] - pos[0]) , abs(self.track [-1][1] - pos[1])
					if distance[0] > 10 or distance[1] > 20:
						#if the airport is near get the airport center point and release the plane, else return the point back
						pos , self.released, self.connected = self.world.check_point_for_airports(pos)
						self.track.append(pos)
				elif self.is_mouse_over():
					self.track.append(pos)
		else:
			self.released = True
	def center(self):
		x = self.x + (self.width / 2)
		y = self.y + (self.height / 2)
		return {'x': x,'y': y}
	def center_point(self):
		x = self.x + (self.width / 2)
		y = self.y + (self.height / 2)
		return (x,y)
	def set_center(self, point):
		self.x = point['x'] - (self.width/2)
		self.y = point['y'] - (self.height/2)
	def rot_center(self,angle):
		"""rotate an image while keeping its center and size"""
		orig_rect = self.sprite["sheet"]["image"].get_rect()
		rot_image = pygame.transform.rotate(self.sprite["sheet"]["image"], angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image
	def rot_center_shadow(self,angle):
		"""rotate an image while keeping its center and size"""
		orig_rect = self.shadow["sheet"]["image"].get_rect()
		rot_image = pygame.transform.rotate(self.shadow["sheet"]["image"], angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image
	def set_landing_path(self, path):
		self.track = path
		self.released = True
	def draw(self, screen):
		if self.landing:
			screen.blit(
				pygame.transform.smoothscale(self.rot_center(self.draw_angle),(int(self.width),int(self.height))),
				 (self.x,self.y),
				  self.sprite["frames"][0])
		else:
			screen.blit(self.rot_center_shadow(self.draw_angle), (self.x + self.world.shadow_offset[0],self.y + self.world.shadow_offset[1]), self.shadow["frames"][0])
			screen.blit(self.rot_center(self.draw_angle), (self.x,self.y), self.sprite["frames"][0])
			
		if self.is_mouse_over():
			pygame.gfxdraw.aacircle(screen, int(self.center()['x']), int(self.center()['y']) ,int(self.width / 2),(255,0,0))
		#for t in self.track:
		#	pygame.gfxdraw.filled_circle(screen, t[0], t[1], 2, (255,255,255))
		self.draw_track(screen)
		#if len(self.track):
		#	pygame.gfxdraw.line(screen, self.center()['x'] , self.center()['y'], self.track[0][0], self.track[0][1], (255,0,0))
	def is_point_inside(self, point):
		center = self.center()
		if (abs(point[0] - center['x']) < 5) and (abs(point[1] - center['y']) < 5):
			return True
	def is_mouse_over(self):
		pos = pygame.mouse.get_pos()
		if (pos[0] > self.x and abs(pos[0] - self.x) < self.width) and (pos[1] > self.y and abs(pos[1] - self.y) < self.height):
			return True
	def draw_track(self,screen):
		if self.connected:
			color = (100,255,100)
		else:
			color = (255,255,255)
		width = 3
		
		if len(self.track) > 2:
			pygame.draw.lines(screen, color, False, self.track, width)
			"""
			for i in range(len(self.track)):
				if i < len(self.track) - 1:
					p1 = self.track[i]
					p2 = self.track[i+1]
					dx = p2[0] - p1[0]
					dy = p2[1] - p1[1]
					distance = max(abs(dx), abs(dy))
					for n in range(distance):
						x = int(p1[0] + int(n)/distance*dx)
						y = int(p1[1] + int(n)/distance*dy)
						pygame.gfxdraw.aacircle(screen,x,y,width,color)
		"""
		
