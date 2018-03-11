import configparser, os
import pygame
from pygame.locals import *
from utils import load_image
from globals import *

class Element(object):
	def __init__(self, name):
		self.name = name
		self.config = configparser.ConfigParser()
		self.config.read(os.path.join(ROOT_PATH,'data','elements',name + '.ini'))
		self.sprite = self.load_sprite(self.config.get('sprite', 'filename'), self.config.getint('sprite', 'frames'))
		if self.config.getboolean('sprite', 'shadow'):
			self.shadow = self.load_sprite(self.config.get('sprite', 'shadow_filename'), self.config.getint('sprite', 'frames'))
	def load_sprite(self, filename , frames_count):
		sprite_sheet = load_image(filename)
		sheet = {"image": sprite_sheet[0], "rect": sprite_sheet[1]}
		frames = []
		self.width = sheet['rect'].width / frames_count
		self.height = sheet['rect'].height
		x = 0
		y = 0
		for i in range(frames_count):
			frames.append(pygame.Rect(x,y,self.width,self.height))
			x += self.width
		return {"sheet":sheet, "frames": frames}
