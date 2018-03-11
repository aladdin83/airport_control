import pygame
from pygame.locals import *

class Camera(object):
	def __init__(self, screen, scene):
		self.center = ((screen.get_width() / 2), (screen.get_height() /2))
		self.focus_rect = Rect(self.center[0] - 75, self.center[1] - 75, 150, 150)
		self.bounding_box = Rect(75 , 75, screen.get_width() - 150, screen.get_height() - 150)
		self.scene = scene
		self.screen = screen
		self.x = 0
		self.y = 0
	def draw(self, screen):
		temp = 0
		#pygame.draw.rect(screen, (0,0,0), self.focus_rect, 2)
		#pygame.draw.rect(screen, (255,0,0) , self.bounding_box, 1)
	def update(self):
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if mouse_x < self.bounding_box.x:
			scroll_speed = self.bounding_box.x - mouse_x
			if scroll_speed > 0:
				self.x += 2
			if scroll_speed >= 30:
				self.x += 5
		elif mouse_x > self.bounding_box.x + self.bounding_box.width:
			scroll_speed = self.bounding_box.x + self.bounding_box.width - mouse_x
			if scroll_speed < 0:
				self.x -= 2
			if scroll_speed <= -30:
				self.x -= 5
		if mouse_y < self.bounding_box.y:
			scroll_speed = self.bounding_box.y - mouse_y
			if scroll_speed > 0:
				self.y += 2
			if scroll_speed >= 30:
				self.y += 5
		elif mouse_y > self.bounding_box.y + self.bounding_box.height:
			scroll_speed = self.bounding_box.y + self.bounding_box.height - mouse_y
			if scroll_speed < 0:
				self.y -= 2
			if scroll_speed <= -30:
				self.y -= 5
		if self.x > 0:
			self.x = 0
		if (self.x * -1) > (self.scene.width - self.screen.get_width()):
			self.x = -1 * (self.scene.width - self.screen.get_width())
		if (self.y + self.screen.get_height() > self.scene.height):
			self.y = self.scene.height - self.screen.get_height()
		if ((-1 * self.y) + self.screen.get_height() > self.scene.height):
			self.y = -1 * (self.scene.height - self.screen.get_height())
