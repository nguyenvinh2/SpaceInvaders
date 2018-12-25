import sys
import pygame
import settings
import ship
import alien
import functions

def game():
  pygame.init()
  game_settings = settings.Settings()
  screen = pygame.display.set_mode((game_settings.width,game_settings.height))
  pygame.display.set_caption("Space Invaders")

  player_render = ship.Ship(screen, game_settings)
  bullets = pygame.sprite.Group()
  #aliens = alien.Alien(game_settings, screen)
  alien_group = pygame.sprite.Group()

  functions.alien_fleet(game_settings, screen, alien_group)

  while True:
      functions.check_events(game_settings, screen, player_render, bullets)
      player_render.update()
      functions.update_bullets(alien_group, bullets, screen, game_settings)
      functions.update_aliens(game_settings, alien_group)
      functions.update_screen(game_settings, screen, player_render, alien_group, bullets)

game()

