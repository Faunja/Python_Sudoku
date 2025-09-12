import pygame

class Define_Controls:
	def __init__(self):
		self.QuitGame = [pygame.K_ESCAPE]
		self.MoveDown = [pygame.K_DOWN, pygame.K_s]
		self.MoveUp = [pygame.K_UP, pygame.K_w]
		self.MoveLeft = [pygame.K_LEFT, pygame.K_a]
		self.MoveRight = [pygame.K_RIGHT, pygame.K_d]
		self.Numbers = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
		self.RestartGame = [pygame.K_r]
		self.Fullscreen = [pygame.K_F11]
		
		self.PressedKeys = {}

Controls = Define_Controls()
