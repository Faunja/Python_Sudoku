import copy
import pygame
import random
from Display.define_display import Display

class define_sudoku:
	def __init__(self):
		self.Grid = [[0 for X in range(9)] for Y in range(9)]
		self.SavedGrids = []
		self.LockedGrid = copy.deepcopy(self.Grid)
		self.CheckGrid = copy.deepcopy(self.Grid)
		self.Position = [4, 4]
		self.PlacePosition = [0, 0]
		self.MouseMove = True
		self.update_cell_display()
		self.create_grid()
	
	def update_cell_display(self):
		GridSize = int(min(Display.DisplayWidth, Display.DisplayHeight) * (4 / 5))
		self.CellWallSize = int(GridSize / 600)
		self.SquareWallSize = int(GridSize / 100) - self.CellWallSize
		WallOffset = self.SquareWallSize * 2 + self.CellWallSize * 6
		self.CellSize = int((GridSize - WallOffset) / 9)
		self.CellOffset = [int((Display.DisplayWidth - self.CellSize * 9 - WallOffset) / 2), int(Display.DisplayHeight - self.CellSize * 9 - WallOffset) / 2]
		self.Font = pygame.font.SysFont("lexend", int(self.CellSize))
	
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
		self.SavedGrids.append(copy.deepcopy(self.Grid))
		X, Y = self.Position
		if self.LockedGrid[Y][X]:
			return
		OldNumber = self.Grid[Y][X]
		if NewNumber == OldNumber:
			return
		self.Grid[Y][X] = NewNumber
		SquarePosition = [int(X / 3) * 3, int(Y / 3) * 3]
		for Column in range(SquarePosition[1], SquarePosition[1] + 3):
			if Column == Y:
				continue
			for Row in range(SquarePosition[0], SquarePosition[0] + 3):
				if Row == X:
					continue
				if self.Grid[Y][X] == self.Grid[Column][Row] and self.Grid[Y][X]:
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
			elif OldNumber == self.Grid[Y][Row] and OldNumber:
				self.CheckGrid[Y][X] -= 1
				self.CheckGrid[Y][Row] -= 1
		self.check_cell_availability([X, Y])
	
	def check_cell_availability(self, Position):
		X, Y = Position
		CellAvailability = [Cell for Cell in range(1, 10)]
		if int(Y / 3) * 3 != Y:
			SquarePosition = [int(X / 3) * 3, int(Y / 3) * 3]
			for Column in range(SquarePosition[1], SquarePosition[1] + 3):
				if Column == Y:
					continue
				for Row in range(SquarePosition[0], SquarePosition[0] + 3):
					if Row == X:
						continue
					if self.Grid[Column][Row] in CellAvailability:
						CellAvailability.remove(self.Grid[Column][Row])
		for Column in range(9):
			if self.Grid[Column][X] in CellAvailability and Y != Column:
				CellAvailability.remove(self.Grid[Column][X])
		for Row in range(9):
			if self.Grid[Y][Row] in CellAvailability and X != Row:
				CellAvailability.remove(self.Grid[Y][Row])
		return CellAvailability
	
	def check_grid_availability(self):
		for Y in range(9):
			for X in range(9):
				AvailableNumbers = self.check_cell_availability([X, Y])
				if len(AvailableNumbers) == 1:
					self.Grid[Y][X] = AvailableNumbers[0]
	
	def check_row_availability(self):
		self.check_grid_availability()
		RowAvailability = []
		for X in range(9):
			RowAvailability.append(self.check_cell_availability([X, self.PlacePosition[1]]))
		for Number in RowAvailability[self.PlacePosition[0]]:
			LastNumber = True
			for X in range(3 + int(self.PlacePosition[0] / 3) * 3, 9):
				if Number in RowAvailability[X]:
					LastNumber = False
					break
			if LastNumber:
				self.Grid[self.PlacePosition[1]][self.PlacePosition[0]] = Number
	
	def restart_grid(self):
		self.Grid = [[0 for X in range(9)] for Y in range(9)]
		self.SavedGrids = []
		self.LockedGrid = copy.deepcopy(self.Grid)
		self.CheckGrid = copy.deepcopy(self.Grid)
		self.PlacePosition = [0, 0]

	def lock_grid(self):
		CellsCut = 0
		while CellsCut < 9 * 9 - 36:
			Position = [random.randrange(9), random.randrange(9)]
			if self.Grid[Position[1]][Position[0]] != 0:
				self.Grid[Position[1]][Position[0]] = 0
				CellsCut += 1
		for Column in range(9):
			for Row in range(9):
				self.LockedGrid[Column][Row] = int(self.Grid[Column][Row] != 0)

	def create_grid(self):
		while self.PlacePosition != [8, 8]:
			self.check_row_availability()
			if not self.Grid[self.PlacePosition[1]][self.PlacePosition[0]]:
				AvailableCells = self.check_cell_availability(self.PlacePosition)
				if not len(AvailableCells):
					self.restart_grid()
					continue
				self.Grid[self.PlacePosition[1]][self.PlacePosition[0]] = random.choice(AvailableCells)
			self.PlacePosition[0] += 1
			if self.PlacePosition[0] == 9:
				self.PlacePosition[0] = 0
				self.PlacePosition[1] += 1
			if self.PlacePosition == [8, 8]:
				self.lock_grid()
		
	def rewind_grid(self):
		if self.PlacePosition == [0, 0] or not len(self.SavedGrids):
			return
		self.Grid = copy.deepcopy(self.SavedGrids[len(self.SavedGrids) - 1])
		self.SavedGrids.pop()
		self.PlacePosition[0] -= 1
		if self.PlacePosition[0] == -1:
			self.PlacePosition[0] = 8
			self.PlacePosition[1] -= 1
	
	def manual_grid(self):
		if self.PlacePosition == [8, 8]:
			return
		self.SavedGrids.append(copy.deepcopy(self.Grid))
		self.check_row_availability()
		if not self.Grid[self.PlacePosition[1]][self.PlacePosition[0]]:
			AvailableCells = self.check_cell_availability(self.PlacePosition)
			if not len(AvailableCells):
				self.SavedGrids.pop()
				return
			self.Grid[self.PlacePosition[1]][self.PlacePosition[0]] = random.choice(AvailableCells)
		if self.PlacePosition == [8, 8]:
			return
		self.PlacePosition[0] += 1
		if self.PlacePosition[0] == 9:
			self.PlacePosition[0] = 0
			self.PlacePosition[1] += 1

Sudoku = define_sudoku()
