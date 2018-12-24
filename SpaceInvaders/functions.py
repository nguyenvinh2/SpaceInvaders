import sys
import pygame

def check_events(player_render):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RIGHT:
        player_render.move_right = True
      if event.key == pygame.K_LEFT:
        player_render.move_left = True
    elif event.type == pygame.KEYUP:
      player_render.move_right = False
      player_render.move_left = False

def update_screen(game_settings, screen, player_render):
      screen.fill(game_settings.background_color)
      player_render.blitme()
      pygame.display.flip()
