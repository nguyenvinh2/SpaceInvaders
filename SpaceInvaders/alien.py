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

  def blitme(self):
    self.screen.blit(self.image, self.rect)
