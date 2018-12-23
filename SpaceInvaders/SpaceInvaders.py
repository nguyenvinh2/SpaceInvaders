import sys
import pygame
import settings
import ship

def game():
  pygame.init()
  game_settings = settings.Settings()
  screen = pygame.display.set_mode((game_settings.width,game_settings.height))
  pygame.display.set_caption("Space Invaders")

  player_render = ship.Ship(screen)

  while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()

      screen.fill(game_settings.background_color)
      player_render.blitme()
      pygame.display.flip()

game()

