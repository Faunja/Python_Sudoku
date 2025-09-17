import time
import pygame
from define_sudoku import Sudoku
from User.define_controls import Controls
from User.define_user import User
from Display.define_display import Display

def update_key_down(Key):
	if Key in Controls.QuitGame:
		User.Playing = False
	
	if Key in Controls.RewindGrid:
		Controls.PressedKeys[Key] = [0, 5, 60]
	if Key in Controls.ForwardGrid:
		Controls.PressedKeys[Key] = [0, 5, 60]
	
	if Key in Controls.MoveDown:
		Controls.PressedKeys[Key] = [0, 5]
	if Key in Controls.MoveUp:
		Controls.PressedKeys[Key] = [0, 5]
	if Key in Controls.MoveLeft:
		Controls.PressedKeys[Key] = [0, 5]
	if Key in Controls.MoveRight:
		Controls.PressedKeys[Key] = [0, 5]
	if Key in Controls.Numbers:
		Sudoku.update_cells(Controls.Numbers.index(Key))
	if Key in Controls.RestartGame:
		Sudoku.restart_grid()
		Sudoku.create_grid()
	if Key in Controls.SolveSudoku:
		Sudoku.solve_grid()
	
	if Key in Controls.Fullscreen:
		Display.toggle_fullscreen()
		Sudoku.update_cell_display()

def update_key_up(Key):
	if Key in Controls.RewindGrid:
		Controls.PressedKeys.pop(Key)
	if Key in Controls.ForwardGrid:
		Controls.PressedKeys.pop(Key)
	if Key in Controls.MoveDown:
		Controls.PressedKeys.pop(Key)
	if Key in Controls.MoveUp:
		Controls.PressedKeys.pop(Key)
	if Key in Controls.MoveLeft:
		Controls.PressedKeys.pop(Key)
	if Key in Controls.MoveRight:
		Controls.PressedKeys.pop(Key)

def check_key(Keybind):
	for Key in Keybind:
		if Key in Controls.PressedKeys:
			return Key
	return False

def update_pressed_time(Keybind):
	Controls.PressedKeys[Keybind][0] = time.time()
	MinWaitTime = 10
	if len(Controls.PressedKeys[Keybind]) > 2:
		MinWaitTime = Controls.PressedKeys[Keybind][2]
	if Controls.PressedKeys[Keybind][1] < MinWaitTime:
		Controls.PressedKeys[Keybind][1] += 1

def check_pressed_key(Keybinds):
	Keybind = check_key(Keybinds)
	if Keybind:
		if time.time() - Controls.PressedKeys[Keybind][0] > 1 / Controls.PressedKeys[Keybind][1]:
			update_pressed_time(Keybind)
			return True
	return False

def update_pressed_keys():
	if check_pressed_key(Controls.RewindGrid):
		Sudoku.undo_update_cells()
	if check_pressed_key(Controls.ForwardGrid):
		Sudoku.redo_update_cells()
	if check_pressed_key(Controls.MoveDown):
		Sudoku.update_position([0, 1])
	if check_pressed_key(Controls.MoveUp):
		Sudoku.update_position([0, -1])
	if check_pressed_key(Controls.MoveLeft):
		Sudoku.update_position([-1, 0])
	if check_pressed_key(Controls.MoveRight):
		Sudoku.update_position([1, 0])


def event_handler():
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				Sudoku.MouseMove = True

		if event.type == pygame.KEYDOWN:
			update_key_down(event.key)

		if event.type == pygame.KEYUP:
			update_key_up(event.key)

		if event.type == pygame.QUIT:
			User.Playing = False

	update_pressed_keys()
	Sudoku.update_position()
