import pygame
pygame.init()
from event_handler import event_handler
from Display.display_game import display_game
from User.define_user import User

def main():
	while User.Playing:
		User.Clock.tick(User.FPS)
		if User.Clock.get_fps() != 0:
			User.AffectiveFPS = User.Clock.get_fps()
		event_handler()
		display_game()
		pygame.display.update()
	pygame.quit()

main()

