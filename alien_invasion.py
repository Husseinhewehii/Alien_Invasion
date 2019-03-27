import pygame
from pygame.sprite import Group
from settings_module import Settings
from ship_module import Ship
import game_functions_module as gf
from game_stats import Game_Stats
from button import Button
from scoreboard import Scoreboard

def run_game():

	#Initialize PyGame ,Settings and screen Object
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
	(ai_settings.screen_width
	,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	#make the ship , group of bullets and a group of aliens
	ship = Ship(ai_settings,screen)
	bullets = Group()
	aliens = Group()

	#make instance of Game_Stats class
	stats = Game_Stats(ai_settings)
						
	
	#make instance of scoreboard
	sb = Scoreboard(ai_settings,screen,stats)
		
	#make the play button
	play_button = Button(ai_settings,screen,"Play")
	
	#create the fleet of aliens
	gf.create_fleet(ai_settings,screen,ship,aliens)
	
	music_theme = pygame.mixer.music.load('Sounds/ambience.wav')
	pygame.mixer.music.play(-1)
	
	#Start The Main loop for the game
	while True:	
		gf.check_events(ai_settings,screen,sb,aliens,stats,play_button,ship,bullets)
		if stats.game_active:
			ship.update_ship()
			gf.update_bullet(ai_settings,screen,stats,sb,ship,bullets,aliens)
			gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)
		gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button,sb)
		
run_game()
