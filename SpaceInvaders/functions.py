import sys
import pygame
import bullet
import alien
import time
import play

def check_events(settings, screen, player_render, bullets, play_button, stats):
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RIGHT:
        player_render.move_right = True
      if event.key == pygame.K_LEFT:
        player_render.move_left = True
      if event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, player_render, bullets)
      if event.key == pygame.K_q:
        pygame.display.quit()
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYUP:
      player_render.move_right = False
      player_render.move_left = False
      player_render.fire = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      check_play_button(stats, play_button, mouse_x, mouse_y)

def check_play_button(stats, play_button, mouse_x, mouse_y):
  button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
  if button_clicked and not stats.game_active:
    stats.game_active = True

def update_screen(game_settings, screen, player_render, aliens, bullets, play_button, stats):
  screen.fill(game_settings.background_color)
  for bullet in bullets.sprites():
    bullet.draw_bullet()
  player_render.blitme()
  aliens.draw(screen)
  if not stats.game_active:
    play_button.draw_button()
  pygame.display.flip()

def fire_bullet(settings, screen, player_render, bullets):
  if len(bullets) < settings.max_bullets:
    new_bullets = bullet.Bullet(settings, screen, player_render)
    bullets.add(new_bullets)

def update_bullets(aliens, bullets, screen, settings):
  bullets.update()
  for bullet in bullets.copy():
    if bullet.rect.bottom <= 0:
      bullets.remove(bullet)
  collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

  if len(aliens) == 0:
    bullets.empty()
    alien_fleet(settings, screen, aliens)

def alien_fleet(settings, screen, aliens):
  alien_init = alien.Alien(settings, screen)
  space_x = settings.width - 3 * alien_init.rect.width
  space_y = settings.height - 3 * alien_init.rect.height
  alien_number = int(space_x / (3*alien_init.rect.width))
  alien_rows = int(space_y/(3*alien_init.rect.height))
  
  for row in range(alien_rows):
    for alien_count in range(alien_number):
      alien_init = alien.Alien(settings, screen)
      alien_init.x = alien_init.rect.width + 3 * alien_init.rect.width * alien_count
      alien_init.y = alien_init.rect.height + 1.25 * alien_init.rect.height * row
      alien_init.rect.x =  alien_init.x
      alien_init.rect.y = alien_init.y
      aliens.add(alien_init)

def update_aliens(settings, stats, player_render, aliens, screen, bullets):
  check_fleet_edge(settings, aliens)
  aliens.update()
  if pygame.sprite.spritecollideany(player_render, aliens):
    ship_hit(settings, stats, screen, player_render, aliens, bullets)
  aliens_bottom(settings, stats, screen, player_render, aliens, bullets)

def check_fleet_edge(settings, aliens):
  for alien_init in aliens.sprites():
    if alien_init.at_edge():
      change_fleet_direction(settings, aliens)
      break

def change_fleet_direction(settings, aliens):
  for alien_init in aliens.sprites():
    alien_init.rect.y += settings.fleet_drop_speed
  settings.fleet_direction *= -1

def ship_hit(settings, stats, screen, ship, aliens, bullets):
  if stats.ships > 0:
    stats.ships -= 1
    aliens.empty()
    bullets.empty()
    alien_fleet(settings, screen, aliens)
    time.sleep(1)
  else:
    stats.game_active = False

def aliens_bottom(settings, stats, screen, ship, aliens, bullets):
  screen_rect = screen.get_rect()
  for alien_init in aliens.sprites():
    if alien_init.rect.bottom >= screen_rect.bottom:
      ship_hit(settings, stats, screen, ship, aliens, bullets)
      break