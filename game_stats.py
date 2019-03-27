filer = 'high_scores.txt'

class Game_Stats():
	""" track statistics for alien invasion """
	
	def __init__(self,ai_settings):
		"""initialize statistics """
		self.ai_settings = ai_settings
		self.reset_stats()
		
		#start alien invasion in an inactive state
		self.game_active = False
		
		#initialize high score
		self.high_score = self.get_high_score()
	
	def get_high_score(self):
	 """get the highest score """
	 with open(filer) as oj:
		 content = oj.read()
		 content = int(content)
		 return content
			
	def reset_stats(self):
		""" initialize statistics that change during game """
		
		#initialize ships allowance
		self.ships_left = self.ai_settings.ships_limit
		
		#initialize score
		self.score = 0
		
		#initialize level
		self.level = 1
