import sys
import pygame
import bullet
import alien
import time
import play

def check_events(settings, screen, player_render, bullets, play_button, stats, aliens, scoreboard):
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
      check_play_button(stats, play_button, mouse_x, mouse_y, settings, screen, aliens, bullets, player_render, scoreboard)

def check_play_button(stats, play_button, mouse_x, mouse_y, settings, screen, aliens, bullets, ship, scoreboard):
  if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
    settings.space_increase = 0
    settings.init_dyn_settings()
    stats.reset_stats()
    alien_fleet(settings, screen, aliens)
    ship.reset_ship()
    stats.game_active = True
    scoreboard.prep_score()
    scoreboard.prep_high_score()
    scoreboard.prep_level()
    scoreboard.prep_ships()
    aliens.empty()
    bullets.empty()
    pygame.mouse.set_visible(False)

def update_screen(game_settings, screen, player_render, aliens, bullets, play_button, stats, scoreboard):
  screen.fill(game_settings.background_color)
  for bullet in bullets.sprites():
    bullet.draw_bullet()
  player_render.blitme()
  aliens.draw(screen)
  scoreboard.show_score()
  if not stats.game_active:
    play_button.draw_button()
  pygame.display.flip()

def fire_bullet(settings, screen, player_render, bullets):
  if len(bullets) < settings.max_bullets:
    new_bullets = bullet.Bullet(settings, screen, player_render)
    bullets.add(new_bullets)


def update_bullets(aliens, bullets, screen, settings, scoreboard, stats):
  bullets.update()
  for bullet in bullets.copy():
    if bullet.rect.bottom <= 0:
      bullets.remove(bullet)
  collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
  if collisions:
    for alien_init in collisions.values():
      stats.score += settings.points
      scoreboard.prep_score()
    check_high_score(stats, scoreboard)

  if len(aliens) == 0:
    settings.space_increase += .15
    bullets.empty()
    settings.increase_difficulty()
    stats.level += 1
    scoreboard.prep_level()
    alien_fleet(settings, screen, aliens)


def alien_fleet(settings, screen, aliens):
  alien_init = alien.Alien(settings, screen)
  space_x = settings.width - 3 * alien_init.rect.width
  space_y = settings.height - (3+settings.space_increase) * alien_init.rect.height
  alien_number = int(space_x / (3*alien_init.rect.width))
  alien_rows = int(space_y/((3+settings.space_increase)*alien_init.rect.height))
  
  for row in range(alien_rows):
    for alien_count in range(alien_number):
      alien_init = alien.Alien(settings, screen)
      alien_init.x = alien_init.rect.width + 3 * alien_init.rect.width * alien_count
      alien_init.y = alien_init.rect.height + (1.25+settings.space_increase) * alien_init.rect.height * row
      alien_init.rect.x =  alien_init.x
      alien_init.rect.y = alien_init.y
      aliens.add(alien_init)

def update_aliens(settings, stats, player_render, aliens, screen, bullets, scoreboard):
  check_fleet_edge(settings, aliens)
  aliens.update()
  if pygame.sprite.spritecollideany(player_render, aliens):
    ship_hit(settings, stats, screen, player_render, aliens, bullets, scoreboard)
  aliens_bottom(settings, stats, screen, player_render, aliens, bullets, scoreboard)

def check_fleet_edge(settings, aliens):
  for alien_init in aliens.sprites():
    if alien_init.at_edge():
      change_fleet_direction(settings, aliens)
      break

def change_fleet_direction(settings, aliens):
  for alien_init in aliens.sprites():
    alien_init.rect.y += settings.fleet_drop_speed
  settings.fleet_direction *= -1

def ship_hit(settings, stats, screen, ship, aliens, bullets, scoreboard):
  if stats.ships > 0:
    stats.ships -= 1
    scoreboard.prep_ships()
    aliens.empty()
    bullets.empty()
    alien_fleet(settings, screen, aliens)
    time.sleep(1)
  else:
    stats.game_active = False
    pygame.mouse.set_visible(True)

def aliens_bottom(settings, stats, screen, ship, aliens, bullets, scoreboard):
  screen_rect = screen.get_rect()
  for alien_init in aliens.sprites():
    if alien_init.rect.bottom >= screen_rect.bottom:
      ship_hit(settings, stats, screen, ship, aliens, bullets, scoreboard)
      break

def check_high_score(stats, scoreboard):
  if stats.score > stats.high_score:
    stats.high_score = stats.score
    scoreboard.prep_high_score()