import copy
import pygame
import random
from Display.define_display import Display

class define_sudoku:
	def __init__(self):
		self.Grid = [[0 for X in range(9)] for Y in range(9)]
		self.LockedGrid = copy.deepcopy(self.Grid)
		self.CheckGrid = copy.deepcopy(self.Grid)
		self.Position = [4, 4]
		self.PlacePosition = [0, 0]
		self.MouseMove = True
		self.update_cell_display()
	
	def update_cell_display(self):
		GridSize = int(min(Display.DisplayWidth, Display.DisplayHeight) * (4 / 5))
		self.WallSize = int(GridSize / 100)
		self.CellSize = int((GridSize - self.WallSize * 2) / 9)
		self.CellOffset = [int((Display.DisplayWidth - self.CellSize * 9 - self.WallSize * 2) / 2), int(Display.DisplayHeight - self.CellSize * 9 - self.WallSize * 2) / 2]
		self.Font = pygame.font.SysFont("impact", int(self.CellSize))
	
	def update_position(self, Direction = [0, 0]):
		if Direction == [0, 0] and self.MouseMove:
			MouseX, MouseY = pygame.mouse.get_pos()
			if self.CellOffset[0] < MouseX < self.CellOffset[0] + self.CellSize * 9 and self.CellOffset[1] < MouseY < self.CellOffset[1] + self.CellSize * 9:
				self.Position[0] = int((MouseX - self.CellOffset[0]) / self.CellSize)
				self.Position[1] = int((MouseY - self.CellOffset[1]) / self.CellSize)
		else:
			self.MouseMove = False
			self.Position[0] += Direction[0] * int(0 <= self.Position[0] + Direction[0] < 9)
			self.Position[1] += Direction[1] * int(0 <= self.Position[1] + Direction[1] < 9)
	
	def update_cells(self, NewNumber):
		X, Y = self.Position
		if self.LockedGrid[Y][X]:
			return
		OldNumber = self.Grid[Y][X]
		if NewNumber == OldNumber:
			return
		self.Grid[Y][X] = NewNumber
		SquarePosition = [int(X / 3) * 3, int(Y / 3) * 3]
		for Column in range(SquarePosition[1], SquarePosition[1] + 3):
			for Row in range(SquarePosition[0], SquarePosition[0] + 3):
				if self.Grid[Y][X] == self.Grid[Column][Row] and (Column != Y or Row != X) and self.Grid[Y][X]:
					self.CheckGrid[Y][X] += 1
					self.CheckGrid[Column][Row] += 1
				elif OldNumber == self.Grid[Column][Row] and OldNumber:
					self.CheckGrid[Y][X] -= 1
					self.CheckGrid[Column][Row] -= 1
		for Column in range(9):
			if self.Grid[Y][X] == self.Grid[Column][X] and Y != Column and self.Grid[Y][X]:
				self.CheckGrid[Y][X] += 1
				self.CheckGrid[Column][X] += 1
			elif OldNumber == self.Grid[Column][X] and OldNumber:
				self.CheckGrid[Y][X] -= 1
				self.CheckGrid[Column][X] -= 1
		for Row in range(9):
			if self.Grid[Y][X] == self.Grid[Y][Row] and X != Row and self.Grid[Y][X]:
				self.CheckGrid[Y][X] += 1
				self.CheckGrid[Y][Row] += 1
			elif OldNumber == self.Grid[Y][Row] and X != Row and OldNumber:
				self.CheckGrid[Y][X] -= 1
				self.CheckGrid[Y][Row] -= 1
	
	def check_cells(self, Position, NewNumber):
		X, Y = Position
		SquarePosition = [int(X / 3) * 3, int(Y / 3) * 3]
		for Column in range(SquarePosition[1], SquarePosition[1] + 3):
			for Row in range(SquarePosition[0], SquarePosition[0] + 3):
				if NewNumber == self.Grid[Column][Row]:
					return False
		for Column in range(9):
			if NewNumber == self.Grid[Column][X]:
				return False
		for Row in range(9):
			if NewNumber == self.Grid[Y][Row]:
				return False
		return True
	
	def restart_grid(self):
		self.Grid = [[0 for X in range(9)] for Y in range(9)]
		self.LockedGrid = copy.deepcopy(self.Grid)
		self.CheckGrid = copy.deepcopy(self.Grid)
		self.PlacePosition = [0, 0]
	
	def brute_force_grid(self):
		self.restart_grid()
		while self.PlacePosition != [0, 9]:
			NewNumber = random.randint(1, 9)
			BannedNumbers = []
			while not self.check_cells(self.PlacePosition, NewNumber):
				BannedNumbers.append(NewNumber)
				NewNumber = random.randint(1, 9)
				if len(set(BannedNumbers)) == 9:
					self.restart_grid()
			self.Grid[self.PlacePosition[1]][self.PlacePosition[0]] = NewNumber
			self.PlacePosition[0] += 1
			if self.PlacePosition[0] == 9:
				self.PlacePosition[0] = 0
				self.PlacePosition[1] += 1
			

Sudoku = define_sudoku()
