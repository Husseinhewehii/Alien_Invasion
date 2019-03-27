import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	""" a class representing and managing an alien """
	
	def __init__(self,ai_settings,screen):
		""" initializing alien's settings """
		super(Alien,self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#load alien image and it's rect attribute
		self.image = pygame.image.load('Images/alien_1.bmp')
		self.rect = self.image.get_rect()
		
		#start each alien at top left corner of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		#store alien's exact position
		self.x = float(self.rect.x)
		
	
		
	def check_edges(self):
		""" return True if alien at age of the screen """
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		if self.rect.left <= 0:
			return True
	
	def update(self):
		""" moving alien to right or left """
		self.x += (self.ai_settings.alien_speed_factor 
		* self.ai_settings.fleet_direction)
		self.rect.x = self.x

	#not in use for now	
	def blitme(self):
		""" draw alien at it's current location """
		self.screen.blit(self.image,self.rect)
		
		
