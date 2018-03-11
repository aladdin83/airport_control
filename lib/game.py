import os
import pygame
import configparser

from globals import *
from pygame.locals import *
from utils import *
from mouse import *
from world import *

NEW_PLANE = USEREVENT + 1

class Game(object):
    def __init__(self):
        self.__initGame()
        while self.running:
            self.clock.tick(self.frame_rate)
            pygame.display.set_caption(self.name + " FPS: " + str(self.clock.get_fps()))
            self.__checkEvents()
            self.__renderScreen()

        self.__exitGame()

    def __initGame(self):
	    pygame.init()
	    self.name = "War and Peas"
	    self.clock = pygame.time.Clock()
	    self.running = True
	    config = configparser.ConfigParser()
	    config.read(os.path.join(ROOT_PATH,'config.ini'))
	    self.frame_rate = config.getint('video', 'framerate')
	    self.screen_width = int(config.get('video', 'resolution').split('X')[0])
	    self.screen_height = int(config.get('video', 'resolution').split('X')[1])
	    self.screen_depth = int(config.get('video', 'resolution').split('X')[2])
	    if config.getboolean('video', 'fullscreen'):
		    self.screen_mode = FULLSCREEN
	    elif config.getboolean('video', 'opengl'):
		    self.screen_mode = OPENGL
	    else:
		    self.screen_mode = 0
	    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height) , self.screen_mode, self.screen_depth)
	    self.fps = self.clock.get_fps()
	    #pygame.mouse.set_visible(False)
	    self.mouse = Mouse()

	    #:testing only area
	    self.runWorld = False
	    #:end of testing area

    def __checkEvents(self):
	    for e in pygame.event.get():
		    if e.type == QUIT:
			    self.running = False

		    elif e.type == KEYDOWN:
			    if e.key == K_ESCAPE:
				    self.running = 0
			    elif e.key == 102:
				    pygame.display.toggle_fullscreen()
		    elif e.type == MOUSEBUTTONDOWN:
			    if e.button == 1:
				    self.mouse.set_state(2)
		    elif e.type == MOUSEBUTTONUP:
			    self.mouse.set_state(0)
		    elif e.type == NEW_PLANE:
			    if self.runWorld: self.world.sendNewPlane()
    def __exitGame(self):
	    self.running = 0

    def __renderScreen(self):
	    if self.runWorld == False:
		    self.world = World('dubai', self.screen)
		    self.runWorld = True
		    pygame.time.set_timer(NEW_PLANE,5000)

	    self.world.update()
	    self.world.draw(self.screen)
	    #self.mouse.draw(self.screen)
	    pygame.display.update()
	    #: end test area
	    pass
