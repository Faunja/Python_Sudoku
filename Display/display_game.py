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
	SquarePosition = [int(Sudoku.Position[0] / 3) * 3, int(Sudoku.Position[1] / 3) * 3]
	CellColor = [240, 240, 240]

	if Sudoku.LockedGrid[CellPosition[1]][CellPosition[0]]:
		CellColor = [CellColor[0] - 45, CellColor[1] - 45, CellColor[2] - 45]

	if CellPosition[0] in [Cell for Cell in range(SquarePosition[0], SquarePosition[0] + 3)] and CellPosition[1] in [Cell for Cell in range(SquarePosition[1], SquarePosition[1] + 3)]:
		CellColor = [CellColor[0] - 45, CellColor[1] - 45, CellColor[2]]
	elif Sudoku.Position[0] == CellPosition[0] or Sudoku.Position[1] == CellPosition[1]:
		CellColor = [CellColor[0] - 45, CellColor[1] - 45, CellColor[2]]

	if CellPosition == Sudoku.Position or Sudoku.Grid[CellPosition[1]][CellPosition[0]] == Sudoku.Grid[Sudoku.Position[1]][Sudoku.Position[0]] and Sudoku.Grid[CellPosition[1]][CellPosition[0]] != 0:
		CellColor = [150, 150, 240]

	pygame.draw.rect(Display.Display, CellColor, (Position[0], Position[1], CellSize, CellSize))
	Available = Sudoku.GridAvailability[CellPosition[1]][CellPosition[0]]
	if Sudoku.Grid[CellPosition[1]][CellPosition[0]] != 0:
		Color = (180 * int(Sudoku.Grid[CellPosition[1]][CellPosition[0]] not in Available), 0, 0)
		draw_text(str(Sudoku.Grid[CellPosition[1]][CellPosition[0]]), [Position[0] + int(CellSize / 2), Position[1] + int(CellSize / 2)], Font = Sudoku.Font, Color = Color)
	else:
		if not Sudoku.ShowGridAvailability:
			Available = Sudoku.PotentialGrid[CellPosition[1]][CellPosition[0]]
		for Number in Available:
			Color = (45, 45, 45)
			NumberPosition = [((Number - 1) % 3 - 1) * (CellSize / 3), (int((Number - 1) / 3) - 1) * (CellSize / 3)]
			TextPosition = [Position[0] + int(CellSize / 2) + NumberPosition[0], Position[1] + int(CellSize / 2) + NumberPosition[1]]
			draw_text(str(Number), [TextPosition[0], TextPosition[1]], Font = Sudoku.AvailableFont, Color = Color)

def draw_sudoku(Sudoku):
	for Column in range(9):
		YPosition = Column * Sudoku.CellSize + int(Column / 3) * Sudoku.SquareWallSize + Column * Sudoku.CellWallSize + Sudoku.CellOffset[1]
		if YPosition < -Sudoku.CellSize or YPosition > Display.DisplayHeight + Sudoku.CellSize:
			continue
		for Row in range(9):
			XPosition = Row * Sudoku.CellSize + int(Row / 3) * Sudoku.SquareWallSize + Row * Sudoku.CellWallSize + Sudoku.CellOffset[0]
			if XPosition < -Sudoku.CellSize or XPosition > Display.DisplayWidth + Sudoku.CellSize:
				continue
			draw_cell([XPosition, YPosition], Sudoku.CellSize, [Row, Column], Sudoku)

def display_game():
	Display.Display.fill((0, 0, 0))
	draw_sudoku(Sudoku)
	draw_text(str(int(User.AffectiveFPS)), (0, 0), (.5, .5))
	
