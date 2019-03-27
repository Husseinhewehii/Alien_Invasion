class Settings():
	#a class to store all settings for alien invasion
	
	def __init__(self):
		#initialize game's settings
		#screen settings
		self.screen_width = 1200
		self.screen_height = 650
		self.bg_color = (230,230,230)
		
		#ship settings
		self.ships_limit = 3

		#bullet settings
		self.bullet_speed_factor = 2
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 3
		
		#alien settings
		self.fleet_drop_speed = 10
		
		
		#initialize the increasing rate
		self.speedup_scale = 1.1
		self.score_scale = 1.5
		
		#initialize the method holding the dynamic attributes
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self):
		""" initialize settings that change throughout the game"""
		#ship settings
		self.ship_speed_factor = 1.5
		
		#alien settings
		self.alien_speed_factor = 1
		
		#bullet settings
		self.bullet_speed_factor = 2
		
		#fleet direction of 1 represents right; and -1 represents left
		self.fleet_direction = 1
		
		#initialize earned points per alien
		self.alien_points = 50
		
	def increase_speed(self):
		""" increase the values by a constant rate """
		self.ship_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
