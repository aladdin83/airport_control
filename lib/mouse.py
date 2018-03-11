
import pygame
from pygame.locals import *
from utils import *

os.path.dirname(__file__)

class Mouse(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.load_sprite()

	def load_sprite(self):
		self.sheet, self.sheet_rect = load_image('CURSORS_SHEET_1.png')
		self.frames = []
		width = self.sheet.get_width() / 4
		height = self.sheet.get_height()
		self.state = 0

		for i in range(3):
			rect = Rect(i * width, 0 , width, height)
			self.frames.append(rect)
			
	def set_state(self, state):
		self.state = state

	def draw(self, screen):
		x, y = pygame.mouse.get_pos()
		x -= 5
		y -= 5
		#x -= self.frames[self.state].width /2
		#y -= self.frames[self.state].height /2
		screen.blit(self.sheet, (x, y), self.frames[self.state])
		
