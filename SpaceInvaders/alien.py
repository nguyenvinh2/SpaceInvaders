import pygame

class Alien(pygame.sprite.Sprite):
  def __init__(self, settings, screen):
    super().__init__()
    self.screen = screen
    self.settings = settings

    self.image = pygame.image.load('assets/spaceinvaders.jpg')
    self.rect = self.image.get_rect()

    self.rect.x = self.rect.width
    self.rect.y = self.rect.height

    self.x = float(self.rect.x)
    self.y = float(self.rect.y)

  def blitme(self):
    self.screen.blit(self.image, self.rect)

  def update(self):
    self.x += (self.settings.alien_speed * self.settings.fleet_direction)
    self.rect.x = self.x
   
  def at_edge(self):
    screen_rect = self.screen.get_rect()
    if self.rect.right >= screen_rect.right:
      return True
    elif self.rect.left <= 0:
      return True
