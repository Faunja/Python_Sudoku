import time
import pygame
from define_sudoku import Sudoku
from User.define_controls import Controls
from User.define_user import User
from Display.define_display import Display

def check_key(Keybind):
	for Key in Keybind:
		if Key in Controls.PressedKeys:
			return Key
	return False

def update_pressed_keys(Keybind):
	Controls.PressedKeys[Keybind][0] = time.time()
	if Controls.PressedKeys[Keybind][1] <  10:
		Controls.PressedKeys[Keybind][1] += 1

def check_pressed_keys():
	MoveDown = check_key(Controls.MoveDown)
	if MoveDown:
		if time.time() - Controls.PressedKeys[MoveDown][0] > 1 / Controls.PressedKeys[MoveDown][1]:
			update_pressed_keys(MoveDown)
			Sudoku.update_position([0, 1])
	MoveUp = check_key(Controls.MoveUp)
	if MoveUp:
		if time.time() - Controls.PressedKeys[MoveUp][0] > 1 / Controls.PressedKeys[MoveUp][1]:
			update_pressed_keys(MoveUp)
			Sudoku.update_position([0, -1])
	MoveLeft = check_key(Controls.MoveLeft)
	if MoveLeft:
		if time.time() - Controls.PressedKeys[MoveLeft][0] > 1 / Controls.PressedKeys[MoveLeft][1]:
			update_pressed_keys(MoveLeft)
			Sudoku.update_position([-1, 0])
	MoveRight = check_key(Controls.MoveRight)
	if MoveRight:
		if time.time() - Controls.PressedKeys[MoveRight][0] > 1 / Controls.PressedKeys[MoveRight][1]:
			update_pressed_keys(MoveRight)
			Sudoku.update_position([1, 0])

def event_handler():
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key in Controls.QuitGame:
				User.Playing = False
			
			if event.key in Controls.MoveDown:
				Controls.PressedKeys[event.key] = [0, 5]
			if event.key in Controls.MoveUp:
				Controls.PressedKeys[event.key] = [0, 5]
			if event.key in Controls.MoveLeft:
				Controls.PressedKeys[event.key] = [0, 5]
			if event.key in Controls.MoveRight:
				Controls.PressedKeys[event.key] = [0, 5]
			if event.key in Controls.Numbers:
				Sudoku.update_cells(Controls.Numbers.index(event.key))
			if event.key in Controls.RestartGame:
				Sudoku.restart_grid()
			
			if event.key in Controls.Fullscreen:
				Display.toggle_fullscreen()
				Sudoku.update_cell_display()

		if event.type == pygame.KEYUP:
			if event.key in Controls.MoveDown:
				Controls.PressedKeys.pop(event.key)
			if event.key in Controls.MoveUp:
				Controls.PressedKeys.pop(event.key)
			if event.key in Controls.MoveLeft:
				Controls.PressedKeys.pop(event.key)
			if event.key in Controls.MoveRight:
				Controls.PressedKeys.pop(event.key)

		if event.type == pygame.QUIT:
			User.Playing = False

	Sudoku.update_position()
	Sudoku.brute_force_grid()
	check_pressed_keys()
