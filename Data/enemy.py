import pygame,os,math

class Basic():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.width = 60
		self.height = 60
		self.vel = 6
		self.health = 100
		self.image_left = pygame.image.load(os.path.join("Assets","basic_left.png")).convert_alpha()
		self.image_right = pygame.image.load(os.path.join("Assets","basic_right.png")).convert_alpha()
		self.facing_left,self.facing_right = False,False
	def draw(self,master,player):
		self.window = master
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		if self.x+self.width/2>player.x+player.width/2:
			self.facing_right = False
			self.facing_left = True
		elif self.x+self.width/2<player.x+player.width/2:
			self.facing_right = True
			self.facing_left = False
		if self.facing_right == True and self.facing_left == False:
			self.enemy = pygame.transform.scale(self.image_right,
				(self.width,self.height))
			self.window.blit(self.enemy,(self.x,self.y))
		elif self.facing_right == False and self.facing_left == True:
			self.enemy = pygame.transform.scale(self.image_left,
				(self.width,self.height))
			self.window.blit(self.enemy,(self.x,self.y))
	def move(self,dt,dx,dy):
		self.dx = dx
		self.dy = dy
		self.angle = math.atan2(self.y-self.dy,self.x-self.dx)
		self.vel_x = math.cos(self.angle)*self.vel
		self.vel_y = math.sin(self.angle)*self.vel
		self.x -= self.vel_x*dt
		self.y -= self.vel_y*dt
class Shooter():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.width,self.height = 42,64
		self.check_width,self.check_height = 500,500
		self.vel = 8
		self.health = 100
		self.image_left = pygame.image.load(os.path.join("Assets","shooter_left.png")).convert_alpha()
		self.image_right = pygame.image.load(os.path.join("Assets","shooter_right.png")).convert_alpha()
		self.facing_left,self.facing_right = False,False
		self.should_move = True
		self.event = pygame.USEREVENT + 2
		pygame.time.set_timer(self.event,1000)
		self.bullets = []
	def draw(self,master,player):
		self.window = master
		self.player = player
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		if self.x+self.width/2>player.x+player.width/2:
			self.facing_right = False
			self.facing_left = True
		elif self.x+self.width/2<player.x+player.width/2:
			self.facing_right = True
			self.facing_left = False
		if self.facing_right == True and self.facing_left == False:
			self.enemy = pygame.transform.scale(self.image_right,
				(self.width,self.height))
			self.window.blit(self.enemy,(self.x,self.y))
		elif self.facing_right == False and self.facing_left == True:
			self.enemy = pygame.transform.scale(self.image_left,
				(self.width,self.height))
			self.window.blit(self.enemy,(self.x,self.y))
		for bullet in self.bullets:
			bullet.draw(self.window)
	def move(self,dt,dx,dy):
		self.dx = dx
		self.dy = dy
		self.angle = math.atan2(self.y-self.dy,self.x-self.dx)
		self.vel_x = math.cos(self.angle)*self.vel
		self.vel_y = math.sin(self.angle)*self.vel
		self.check_rect = pygame.Rect(self.x-self.check_width/2,self.y-self.check_height/2,
			self.check_width,self.check_height)
		if self.check_rect.colliderect(self.player.rect):
			if self.x+self.width<self.window.get_width() and self.x>0:
				if self.y>0 and self.y+self.height<self.window.get_height():
					self.should_move = False
		if self.should_move == True:
			self.x -= self.vel_x*dt
			self.y -= self.vel_y*dt
		for bullet in self.bullets:
			bullet.move(dt)
			if bullet.rect.colliderect(self.player.rect):
				self.player.get_damage(50)
				self.bullets.remove(bullet)