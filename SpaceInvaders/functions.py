import sys
import pygame
import bullet
import alien

def check_events(settings, screen, player_render, bullets):
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

def update_screen(game_settings, screen, player_render, aliens, bullets):
  screen.fill(game_settings.background_color)
  for bullet in bullets.sprites():
    bullet.draw_bullet()
  player_render.blitme()
  aliens.draw(screen)
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

def update_aliens(settings, aliens):
  check_fleet_edge(settings, aliens)
  aliens.update()

def check_fleet_edge(settings, aliens):
  for alien_init in aliens.sprites():
    if alien_init.at_edge():
      change_fleet_direction(settings, aliens)
      break

def change_fleet_direction(settings, aliens):
  for alien_init in aliens.sprites():
    alien_init.rect.y += settings.fleet_drop_speed
  settings.fleet_direction *= -1