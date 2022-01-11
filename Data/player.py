import pygame,os

class Player():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.width = 44
		self.height = 83
		self.damage_sound = pygame.mixer.Sound(os.path.join("Sounds","hurt.ogg"))
		self.health_sound = pygame.mixer.Sound(os.path.join("Sounds","health.ogg"))
		self.player_image = pygame.image.load(	
			os.path.join("Assets","player.png")).convert_alpha()
		self.player_left_image = pygame.image.load(
			os.path.join("Assets","player_left.png")).convert_alpha()
		self.player_right_image = pygame.image.load(
			os.path.join("Assets","player_right.png")).convert_alpha()
		self.vel = 12
		self.can_left,self.can_right,self.can_up,self.can_down = True,True,True,True
		self.facing_left,self.facing_right = False,False
		self.maximum_health = 1000
		self.current_health = 1000
		self.health_bar_length = 500
		self.health_ratio = self.maximum_health/self.health_bar_length
	def draw(self,master):
		self.window = master
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		if self.facing_left == True and self.facing_right == False:
			self.player = pygame.transform.scale(
				self.player_left_image,(self.width,self.height))
			self.window.blit(self.player,(self.x,self.y))
		if self.facing_left == False and self.facing_right == True:
			self.player = pygame.transform.scale(
				self.player_right_image,(self.width,self.height))
			self.window.blit(self.player,(self.x,self.y))
		self.health_rect = pygame.Rect(10,10,self.current_health/self.health_ratio,25)
		pygame.draw.rect(self.window,'red',self.health_rect)
		self.health_border = pygame.Rect(10,10,self.health_bar_length,25)
		pygame.draw.rect(self.window,'white',self.health_border,width=4)
	def get_damage(self,amount):
		if self.current_health > 0:
			self.current_health -= amount
		if self.current_health <= 0:
			self.current_health = 0
		self.damage_sound.set_volume(0.2)
		self.damage_sound.play()
	def get_health(self,amount):
		if self.current_health < self.maximum_health:
			self.current_health += amount
		if self.current_health >= self.maximum_health:
			self.current_health = self.maximum_health
		self.health_sound.set_volume(0.5)
		self.health_sound.play()