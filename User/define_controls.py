import pygame

class Define_Controls:
	def __init__(self):
		self.QuitGame = [pygame.K_ESCAPE]
		self.RewindGrid = [pygame.K_z]
		self.ForwardGrid = [pygame.K_y]
		self.MoveDown = [pygame.K_DOWN, pygame.K_s]
		self.MoveUp = [pygame.K_UP, pygame.K_w]
		self.MoveLeft = [pygame.K_LEFT, pygame.K_a]
		self.MoveRight = [pygame.K_RIGHT, pygame.K_d]
		self.Numbers = [pygame.K_1, pygame.K_KP1, pygame.K_2, pygame.K_KP2, pygame.K_3, pygame.K_KP3, pygame.K_4, pygame.K_KP4, pygame.K_5, pygame.K_KP5, pygame.K_6, pygame.K_KP6, pygame.K_7, pygame.K_KP7, pygame.K_8, pygame.K_KP8, pygame.K_9, pygame.K_KP9]
		self.RemoveNumbers = [pygame.K_0, pygame.K_KP0, pygame.K_BACKSPACE]
		self.ShowGridAvailability = [pygame.K_q]
		self.PlacePotentialNumbers = [pygame.K_LSHIFT, pygame.K_RSHIFT]
		self.RestartGame = [pygame.K_r]
		self.Fullscreen = [pygame.K_F11]
		
		self.PressedKeys = {}

Controls = Define_Controls()
