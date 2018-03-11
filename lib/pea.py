import random
from element import *

class Pea(Element):
	def __init__(self, name ,startpos):
		Element.__init__(self, name)
		self.x, self.y = startpos

		self.eyes = self.load_sprite(self.config.get('eyes','filename'),self.config.getint('eyes','frames'))
		self.eyes["position"] = {"x": self.config.getint('eyes', 'pos_x'), "y": self.config.getint('eyes', 'pos_y')}
		self.eyes["state"] = 0
		self.eyes["blink"] = self.config.getboolean('eyes', 'blink')
		self.eyes["blinking"] = 0

		self.helmet = self.load_sprite(self.config.get('helmet','filename'), self.config.getint('helmet', 'frames'))
		self.helmet["position"] = {'x': self.config.getint('helmet','pos_x'), 'y': self.config.getint('helmet', 'pos_y')}
		self.helmet["state"] = 0

		self.grabbed = False
		
	def blink(self):
		if self.eyes["blinking"]:
			self.eyes["blinking_frames"] -= 1
			if self.eyes["blinking_frames"] <= 0:
				self.eyes["state"] = 0
				self.eyes["blinking"] = False
		elif self.eyes["blink"]:
			if(random.randint(0, 300) == 0):
				self.eyes["state"] = 1
				self.eyes["blinking"] = True
				self.eyes["blinking_frames"] = 20

	def update(self):
		self.blink()

		if self.grabbed:
			self.x, self.y = pygame.mouse.get_pos()
		
	def draw(self, screen, camera):
		if self.grabbed:
			drawx = self.x
			drawy = self.y
		else:
			drawx = self.x + camera.x
			drawy = self.y + camera.y
			
		screen.blit(self.sprite["sheet"]["image"], (drawx,drawy), self.sprite["frames"][0])
		screen.blit(self.helmet["sheet"]["image"], (drawx + self.helmet["position"]["x"] , drawy + self.helmet["position"]["y"]), self.helmet["frames"][self.helmet["state"]])
		screen.blit(self.eyes["sheet"]["image"], (drawx + self.eyes["position"]["x"],drawy + self.eyes["position"]["y"]), self.eyes["frames"][self.eyes["state"]])
	
