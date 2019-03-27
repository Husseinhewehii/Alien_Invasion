import sys
from time import sleep
import pygame
from bullet_module import Bullet
from alien_module import Alien
filer = 'high_scores.txt'

def prep_alien_hit_sound():
	""" initialize alien hit sound atribute and play it """
	alien_hit_sound = pygame.mixer.Sound('Sounds/alien_hit.wav')
	alien_hit_sound.play()
		
def prep_bullet_sound(stats):
	""" initialize bullet sound attribute and play it """
	if stats.game_active:
		bullet_sound = pygame.mixer.Sound('Sounds/laser.wav')
		bullet_sound.play()
	
def fire_bullet(ai_settings,screen,ship,bullets,stats):
	""" fire the bullet within the allowance """
	#create a new bullet and add to the bullets group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		prep_bullet_sound(stats)
		bullets.add(new_bullet)

def start_game(event,ai_settings,screen,sb,ship,aliens,bullets,stats):
	""" starts the game whenever 'p' key is pressed if game is inactive """
	
	if not stats.game_active:
		#hide the mouse cursor
		pygame.mouse.set_visible(False)
			
		#reset the game's statistics
		stats.reset_stats()
		stats.game_active = True
			
		aliens.empty()
		bullets.empty()
		
		#display ships left and currnet level and score
		sb.prep_images()
			
		#create a new fleet and center the ship and reset values
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		ai_settings.initialize_dynamic_settings()
		
def record_high_score(stats):
	""" add highscores to text file """
	with open (filer) as obj:
		content = obj.read()
		content = int(content)
		if stats.high_score > content:
			with open (filer,'w') as oj:
				oj.write(str(stats.high_score))
	
		
def check_keydown_events(event,ai_settings,screen,sb
,ship,aliens,bullets,stats):
	""" respond to keypresses """
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets,stats)
	elif event.key == pygame.K_q:
		record_high_score(stats)
		sys.exit()
	elif event.key == pygame.K_r:
		start_game(event,ai_settings,screen,sb
		,ship,aliens,bullets,stats)
	elif event.key == pygame.K_p:
		if stats.game_active:
			sb.pause = True
			stats.game_active = False
	elif event.key == pygame.K_c:
		if not stats.game_active:
			stats.game_active = True
			
def check_keyup_events(event,ship):
	""" respond to keyreleases """
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
					
def check_events(ai_settings,screen,sb
,aliens,stats,play_button,ship,bullets):
	"""respond to mouse and keyboard events"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			record_high_score(stats)
			sys.exit()
			
		elif event.type == pygame.KEYDOWN:	
			check_keydown_events(event,ai_settings,screen,sb
			,ship,aliens,bullets,stats)
				
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
			
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,sb
			,ship,bullets,aliens,stats,play_button,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,sb
,ship,bullets,aliens,stats,play_button,mouse_x,mouse_y):
	""" start a new game when player click play button """
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	
	# reset if play button is clicked and game is not active
	if button_clicked and not stats.game_active:
		
		#hide the mouse cursor
		pygame.mouse.set_visible(False)
		
		#reset the game's statistics
		stats.reset_stats()
		stats.game_active = True
		
		aliens.empty()
		bullets.empty()
		
		#display ships left and current level and score
		sb.prep_images()
		
		#create a new fleet and center the ship and reset values
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		ai_settings.initialize_dynamic_settings()
			
def update_bullet(ai_settings,screen,stats,sb,ship,bullets,aliens):
	""" update bullet position and getrid of old bullets """
	
	#update bullet position
	bullets.update()
	
	#getrid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	#check if any bullet hits an alien
	#if so get rid of both
	check_bullet_alien_collision(ai_settings,screen,stats,sb
	,ship,bullets,aliens)

def check_bullet_alien_collision(ai_settings,screen,stats,sb
,ship,bullets,aliens):
	""" checks if a bullet hits an alien and removes both if so """
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	
	#increase score and rerender image if collision occured
	if collisions:
		for alien in collisions.values():
			stats.score += ai_settings.alien_points*len(alien)
			sb.prep_score()
			prep_alien_hit_sound()
		check_high_score(stats,sb)
	next_level(ai_settings,screen,stats,sb,ship,bullets,aliens)	

def next_level(ai_settings,screen,stats,sb,ship,bullets,aliens):
	""" changes with the each fleet destruction """	
	if len(aliens) == 0:
			#destory existing bullets and speed game up
			#increment and display level and create new fleet
			bullets.empty()
			ai_settings.increase_speed()
			stats.level += 1
			sb.prep_level()
			create_fleet(ai_settings,screen,ship,aliens)
						
def check_high_score(stats,sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		
def get_number_aliens_x(ai_settings,alien_width):
	""" find the number of aliens in a row"""
	available_space_x = ai_settings.screen_width - (2*alien_width)
	number_aliens_x = int(available_space_x / (2*alien_width))
	return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
	""" determine number of rows of aliens that fit into the screen """
	available_space_y = (ai_settings.screen_height -(3*alien_height)
	-ship_height)
	number_rows = int(available_space_y / (2*alien_height))
	return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	""" create an alien and place it in a row """
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2*alien_width*alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 *alien.rect.height*row_number
	aliens.add(alien)
	
def create_fleet(ai_settings,screen,ship,aliens):
	""" create a fleet full of aliens """
	#find number of aliens in a row
	#spacing between each alien is equal to one alien width
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height
	,alien.rect.height)
	
	#create a fleet of aliens
	for row_number in range(number_rows):
		#create the first row of aliens
		for alien_number in range(number_aliens_x):
			#create an alien and place it in a row
			create_alien(ai_settings,screen,aliens,alien_number
			,row_number)

def check_fleet_edges(ai_settings,aliens):
	""" respond appropriately if any alien reached the edge """
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	""" drop fleet and change its direction """
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *=-1

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
	""" respond to ship being hit by an alien"""
	
	if stats.ships_left > 0:
		#decrement ships left
		stats.ships_left -= 1
		
		#empty list of aliens and bullets
		aliens.empty()
		bullets.empty()
		
		#create a new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		
		#display ships left
		sb.prep_ships()
		
		#pause
		sleep(0.5)
	else:
		stats.game_active = False

		
def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
	""" checks and responds if any aliens reached the bottom """
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#treat this the same as if a ship got hit
			ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
			break
	
def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
	""" update position of all aliens in the fleet """
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	#check if there is ship-alien collision
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
	
	#look for aliens hitting bottom of the screen
	check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)

def update_screen(ai_settings,screen,stats,ship,aliens
		,bullets,play_button,sb):
	""" update images on the screen and flip to new screen """
	
	#redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)
	
	#draw score information
	sb.show_score()
	sb.show_pause()
	
	if not stats.game_active:
		pygame.mouse.set_visible(True)
	#redraw bullets behind ship and aliens
	bullets.draw(screen)
	
	ship.blitme()
	aliens.draw(screen)
	
	#draw play button if game is inactive
	if not stats.game_active:
		play_button.draw_button()
	else:
		sb.pause = False
		
	#make most recently drawn screen visible
	pygame.display.flip()
