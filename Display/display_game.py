import pygame
from define_sudoku import Sudoku
from User.define_user import User
from Display.define_display import Display

def draw_text(Text, Position, Orientation = [0, 0], Font = Display.Font, Color = (255, 255, 255)):
	Text = Font.render(Text, True, Color)
	TextWidth, TextHeight = Text.get_size()
	Orientation = [TextWidth * (Orientation[0] - .5), TextHeight * (Orientation[1] - .5)]
	Display.Display.blit(Text, (Position[0] + Orientation[0], Position[1] + Orientation[1]))
	return TextWidth, TextHeight

def draw_cell(Position, CellSize, CellPosition, Sudoku):
	Pattern = 15 * int(CellPosition[0] % 2 ^ CellPosition[1] % 2)
	SquarePosition = [int(Sudoku.Position[0] / 3) * 3, int(Sudoku.Position[1] / 3) * 3]
	if Sudoku.LockedGrid[CellPosition[1]][CellPosition[0]]:
		CellColor = (120 - Pattern, 120 - Pattern, 120 - Pattern)
	elif CellPosition == Sudoku.Position or Sudoku.Grid[Sudoku.Position[1]][Sudoku.Position[0]] == Sudoku.Grid[CellPosition[1]][CellPosition[0]] and Sudoku.Grid[Sudoku.Position[1]][Sudoku.Position[0]] != 0:
		CellColor = (120, 120, 210)
	elif CellPosition[0] in [Cell for Cell in range(SquarePosition[0], SquarePosition[0] + 3)] and CellPosition[1] in [Cell for Cell in range(SquarePosition[1], SquarePosition[1] + 3)]:
		CellColor = (180 - Pattern, 180 - Pattern, 210 - Pattern)
	elif Sudoku.Position[0] == CellPosition[0] or Sudoku.Position[1] == CellPosition[1]:
		CellColor = (180 - Pattern, 180 - Pattern, 210 - Pattern)
	else:
		CellColor = (210 - Pattern, 210 - Pattern, 210 - Pattern)
	pygame.draw.rect(Display.Display, CellColor, (Position[0], Position[1], CellSize, CellSize))
	if Sudoku.Grid[CellPosition[1]][CellPosition[0]] != 0:
		Color = (180 * int(Sudoku.CheckGrid[CellPosition[1]][CellPosition[0]] != 0), 0, 0)
		draw_text(str(Sudoku.Grid[CellPosition[1]][CellPosition[0]]), [Position[0] + int(CellSize / 2), Position[1] + int(CellSize / 2)], Font = Sudoku.Font, Color = Color)

def draw_sudoku(Sudoku):
	for Column in range(9):
		YPosition = Column * Sudoku.CellSize + int(Column / 3) * Sudoku.WallSize + Sudoku.CellOffset[1]
		if YPosition < -Sudoku.CellSize or YPosition > Display.DisplayHeight + Sudoku.CellSize:
			continue
		for Row in range(9):
			XPosition = Row * Sudoku.CellSize + int(Row / 3) * Sudoku.WallSize + Sudoku.CellOffset[0]
			if XPosition < -Sudoku.CellSize or XPosition > Display.DisplayWidth + Sudoku.CellSize:
				continue
			draw_cell([XPosition, YPosition], Sudoku.CellSize, [Row, Column], Sudoku)

def display_game():
	Display.Display.fill((0, 0, 0))
	draw_sudoku(Sudoku)
	draw_text(str(int(User.AffectiveFPS)), (0, 0), (.5, .5))
	
