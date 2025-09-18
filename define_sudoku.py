import copy
import pygame
import random
from Display.define_display import Display

class define_sudoku:
	def __init__(self):
		self.Grid = [[0 for X in range(9)] for Y in range(9)]
		self.GridAvailability = [[[Z for Z in range(1, 10)] for X in range(9)] for Y in range(9)]
		self.Position = [4, 4]
		self.MouseMove = True
		
		self.SavedGrids = []
		self.SavePosition = -1
		
		self.LockedGrid = [[1 for X in range(9)] for Y in range(9)]
		self.PlacePosition = [0, 0]
		
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
	
	def check_cell_availability(self, Position):
		X, Y = Position
		CellAvailability = [Cell for Cell in range(1, 10)]
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
	
	def update_cell_availability(self, Position):
		X, Y = Position
		CellAvailability = [Cell for Cell in range(1, 10)]
		SquarePosition = [int(X / 3) * 3, int(Y / 3) * 3]
		for Column in range(SquarePosition[1], SquarePosition[1] + 3):
			if Column == Y:
				continue
			for Row in range(SquarePosition[0], SquarePosition[0] + 3):
				if Row == X:
					continue
				self.GridAvailability[Column][Row] = self.check_cell_availability([Row, Column])
		for Column in range(9):
			if Y != Column:
				self.GridAvailability[Column][X] = self.check_cell_availability([X, Column])
		for Row in range(9):
			self.GridAvailability[Y][Row] = self.check_cell_availability([Row, Y])
	
	def update_grid_availability(self):
		for Column in range(9):
			for Row in range(9):
				self.GridAvailability[Column][Row] = self.check_cell_availability([Row, Column])
	
	def update_cells(self, NewNumber):
		X, Y = self.Position
		if self.LockedGrid[Y][X]:
			return
		OldNumber = self.Grid[Y][X]
		if NewNumber == OldNumber:
			return
		if self.SavePosition + 1 < len(self.SavedGrids):
			self.Sa
			vedGrids = self.SavedGrids[:self.SavePosition + 2]
		self.Grid[Y][X] = NewNumber
		self.update_cell_availability(self.Position)
		self.SavePosition += 1
		self.SavedGrids.append(copy.deepcopy(self.Grid))
	
	def undo_update_cells(self):
		if self.SavePosition < 0:
			return
		self.Grid = copy.deepcopy(self.SavedGrids[self.SavePosition])
		self.SavePosition -= 1
	
	def redo_update_cells(self):
		if self.SavePosition >= len(self.SavedGrids) - 1:
			return
		self.SavePosition += 1
		self.Grid = copy.deepcopy(self.SavedGrids[self.SavePosition])
	
	def check_availability(self, Position):
		for Y in range(9):
			for X in range(9):
				AvailableNumbers = self.check_cell_availability([X, Y])
				if len(AvailableNumbers) == 1:
					self.Grid[Y][X] = AvailableNumbers[0]
		RowAvailability = []
		for X in range(9):
			RowAvailability.append(self.check_cell_availability([X, Position[1]]))
		for Number in RowAvailability[Position[0]]:
			LastNumber = True
			for X in range(3 + int(Position[0] / 3) * 3, 9):
				if Number in RowAvailability[X]:
					LastNumber = False
					break
			if LastNumber:
				self.Grid[Position[1]][Position[0]] = Number
	
	def restart_grid(self):
		self.Grid = [[0 for X in range(9)] for Y in range(9)]
		self.SavedGrids = []
		self.SavePosition = -1
		self.LockedGrid = [[1 for X in range(9)] for Y in range(9)]

	def solve_grid(self):
		AvailableChoice = [[0 for X in range(9)] for Y in range(9)]
		for Column in range(9):
			for Row in range(9):
				if self.LockedGrid[Column][Row]:
					continue
				Available = self.check_cell_availability([Row, Column])
				if not len(Available):
					continue
				self.Grid[Column][Row] = Available[AvailableChoice[Column][Row]]
				self.SavePosition += 1
				self.SavedGrids.append(copy.deepcopy(self.Grid))

	def lock_grid(self):
		CellsRemoved = 0
		SolvedGrid = copy.deepcopy(self.Grid)
		while CellsRemoved < 9 * 9 - 36:
			Position = [random.randint(0, 8), random.randint(0, 8)]
			if self.LockedGrid[Position[1]][Position[0]]:
				self.Grid[Position[1]][Position[0]] = 0
				self.LockedGrid[Position[1]][Position[0]] = 0
				CellsRemoved += 1
				self.SavePosition += 1
				self.SavedGrids.append(copy.deepcopy(self.Grid))

	def create_grid(self):
		PlacePosition = [0, 0]
		while PlacePosition != [8, 8]:
			self.check_availability(PlacePosition)
			if not self.Grid[PlacePosition[1]][PlacePosition[0]]:
				AvailableCells = self.check_cell_availability(PlacePosition)
				if not len(AvailableCells):
					PlacePosition = [0, 0]
					self.restart_grid()
					continue
				self.Grid[PlacePosition[1]][PlacePosition[0]] = random.choice(AvailableCells)
			PlacePosition[0] += 1
			if PlacePosition[0] == 9:
				PlacePosition[0] = 0
				PlacePosition[1] += 1
		self.lock_grid()
		self.SavePosition = 0
		self.SavedGrids = [copy.deepcopy(self.Grid)]
		self.update_grid_availability()

Sudoku = define_sudoku()






















