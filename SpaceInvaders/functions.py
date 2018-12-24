import sys
import pygame
import bullet

def check_events(settings, screen, player_render, bullets):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RIGHT:
        player_render.move_right = True
      if event.key == pygame.K_LEFT:
        player_render.move_left = True
      if event.key == pygame.K_SPACE:
        new_bullets = bullet.Bullet(settings, screen, player_render)
        bullets.add(new_bullets)
    elif event.type == pygame.KEYUP:
      player_render.move_right = False
      player_render.move_left = False

def update_screen(game_settings, screen, player_render, bullets):
      screen.fill(game_settings.background_color)
      for bullet in bullets.sprites():
        bullet.draw_bullet()
      player_render.blitme()
      pygame.display.flip()