import pygame.font
from pygame.sprite import Group
from ship_module import Ship

class Scoreboard():
	""" class reports scoring information """
	
	def __init__(self,ai_settings,screen,stats):
		""" initializing scorekeeping attributes """
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		#font setting for scoring info
		self.text_color = (0,100,250)
		self.text_ins = (250,250,250)
		self.bg_ins = (0,0,0)
		self.font = pygame.font.SysFont(None,40)
		self.font_2 = pygame.font.SysFont(None,20)
		
		#prepare images
		self.prep_images()
		
		# prepare pause imase
		self.prep_pause_ins()
		
		#draw pause flag
		self.pause = False
	
		
	def prep_images(self):
		#prepare initial score image
		self.prep_score()
		self.prep_high_score()
		
		#prepare initial level
		self.prep_level()
		
		#prepare ships allowance display
		self.prep_ships()
	
	def prep_score(self):
		""" turn score into a rendered image """
		rounded_score = int(round(self.stats.score,-1))
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str,True
		,self.text_color,self.ai_settings.bg_color)
		
		#display score at top right of screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
	
	def prep_high_score(self):
		""" turn high score into rendered image """
		rounded_high_score = int(round(self.stats.high_score,-1))
		high_score_str = "{:,}".format(rounded_high_score)
		self.high_score_image = self.font.render(high_score_str,True
		,self.text_color,self.ai_settings.bg_color)
		
		#display high score at screen top
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.screen_rect.top
	
	def prep_level(self):
		"""turn level value into a rendered image """
		self.level_image = self.font.render(str(self.stats.level),True
		,self.text_color,self.ai_settings.bg_color)
		
		#display level below score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom +10
	
	def prep_ships(self):
		self.ships = Group()
		for ship_num in range(self.stats.ships_left):
			ship = Ship(self.ai_settings,self.screen)
			ship.rect.x = 10 + ship.rect.width*ship_num
			ship.rect.y = 10
			self.ships.add(ship)
	
	def prep_pause_ins(self):
		""" prepare instructions image"""
		self.pause_image = self.font.render("press 'c' to continue,'p'" 
		+" to pause or 'r' to restart",True,self.text_ins,self.bg_ins)
		
		#display instructions msg on screen top
		self.pause_rect = self.pause_image.get_rect()
		self.pause_rect.centerx = self.screen_rect.centerx
		self.pause_rect.top = 40
	
	def show_score(self):
		""" draw score to screen """
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		self.ships.draw(self.screen)
	
	def show_pause(self):
		if self.pause:
			pygame.mouse.set_visible(True)
			self.screen.blit(self.pause_image,self.pause_rect)
		if not self.pause :
			pygame.mouse.set_visible(False)
