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
  bullets = pygame.sprite.Group()

  while True:
      functions.check_events(game_settings, screen, player_render, bullets)
      player_render.update()
      bullets.update()

      for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
          bullets.remove(bullet)

      functions.update_screen(game_settings, screen, player_render, bullets)

game()

