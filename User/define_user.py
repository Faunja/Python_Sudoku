import pygame

class Define_User:
	def __init__(self):
		self.FPS = 60 
		self.AffectiveFPS = self.FPS
		self.Clock = pygame.time.Clock()
		self.Playing = True

User = Define_User()

