import pygame

class Define_Display:
	def __init__(self):
		self.Fullscreen = False
		Screen = pygame.display.get_desktop_sizes()
		self.ScreenWidth = Screen[0][0]
		self.ScreenHeight = Screen[0][1]
		
		self.DisplayDifference = 4 / 5
		self.DisplayWidth = self.ScreenWidth * self.DisplayDifference
		self.DisplayHeight = self.ScreenHeight * self.DisplayDifference
		
		self.update_display()

	def update_display(self):
		if self.Fullscreen == False:
			self.Display = pygame.display.set_mode((self.DisplayWidth, self.DisplayHeight))
		else:
			self.Display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.Font = pygame.font.SysFont("lexend", int(min(self.DisplayWidth, self.DisplayHeight) / 16))
	
	def update_display_resolution(self, Width, Height):
		self.DisplayWidth = Width
		self.DisplayHeight = Height
		self.update_display()
	
	def toggle_fullscreen(self):
		self.Fullscreen = not self.Fullscreen
		if self.Fullscreen:
			self.OldDisplay = [self.DisplayWidth, self.DisplayHeight]
			self.update_display_resolution(self.ScreenWidth, self.ScreenHeight)
		else:
			self.update_display_resolution(self.OldDisplay[0], self.OldDisplay[1])

Display = Define_Display()
