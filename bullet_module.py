import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	""" a class to manage bullets fired from the ship """
	
	def __init__(self,ai_settings,screen,ship):
		""" create a bullet object at the ship's current position """
		super(Bullet,self).__init__()
		self.screen = screen
		
		#create bullet rect at (0,0) then set correct position
		#self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
		self.image = pygame.image.load('Images/the_rocket.bmp')
		self.rect = self.image.get_rect()
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		
		#store the bullet's position as a decimal value
		self.y = float(self.rect.y)
		
		self.rect_color = ai_settings.bullet_color
		self.rect_speed_factor = ai_settings.bullet_speed_factor
			
		
	def update(self):
		""" move the bullet up the screen """
		
		#update decimal position of the bullet
		self.y -= self.rect_speed_factor
		
		#update the main rect variable position
		self.rect.y = self.y
	
	#not in use
	def draw_bullet(self):
		""" draw bullet to the screen """
		pygame.draw.rect(self.screen,self.rect_color,self.rect)
