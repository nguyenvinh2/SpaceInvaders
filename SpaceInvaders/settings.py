class Settings():
  def __init__(self):
    self.width = 1280
    self.height = 720
    self.background_color = (0,0,0)
    self.ship_speed = .8

    self.bullet_speed = 1
    self.bullet_width = 2
    self.bullet_height = 5
    self.bullet_color = 255,255,255
    self.max_bullets = 10

    self.alien_speed = .5
    self.fleet_drop_speed = 10
    self.fleet_direction = 1

    self.ship_limit = 2

    self.speedup = 1.1
    self.init_dyn_settings()

    self.increase_score = 10

    self.space_increase = 0

  def init_dyn_settings(self):
    self.ship_speed = .8
    self.bullet_speed = 1
    self.alien_speed = .5
    self.fleet_direction = 1
    self.points = 10

  def increase_difficulty(self):
    self.alien_speed *= self.speedup
    self.ship_speed += .15
    self.bullet_speed += .15
    self.points += self.increase_score