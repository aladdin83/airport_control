import pygame

class Airport:
	def __init__(self, rect, landing_path):
		self.rect = rect
		self.landing_path = landing_path
	def get_landing_path(self):
		landing_path = []
		for p in self.landing_path:
			landing_path.append(p)
		return landing_path
	def check_plane_collide(self, plane):
		plane_center = plane.center_point()
		if self.rect.collidepoint(plane_center):
			return True
		else:
			return False
