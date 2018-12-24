import sys
import pygame
import settings
import ship
import functions

def game():
  pygame.init()
  game_settings = settings.Settings()
  screen = pygame.display.set_mode((game_settings.width,game_settings.height))
  pygame.display.set_caption("Space Invaders")

  player_render = ship.Ship(screen, game_settings)

  while True:
      functions.check_events(player_render)
      player_render.update()
      functions.update_screen(game_settings, screen, player_render)

game()

