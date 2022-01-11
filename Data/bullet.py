import pygame,os,math

class Bullet():
	def __init__(self,x,y,dx,dy):
		self.x = x
		self.y = y
		self.width = 30
		self.height = 30
		self.vel = 15
		self.angle = math.atan2(self.y-dy,self.x-dx)
		self.vel_x = math.cos(self.angle)*self.vel
		self.vel_y = math.sin(self.angle)*self.vel
		self.bullet_image = pygame.image.load(
			os.path.join("Assets","plasma.png")).convert_alpha()
	def draw(self,master):
		self.window = master
		self.bullet = pygame.transform.scale(self.bullet_image,(self.width,self.height))
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.window.blit(self.bullet,(self.x,self.y))
	def move(self,dt):
		self.x -= self.vel_x*dt
		self.y -= self.vel_y*dt

class Enemy_Bullet():
	def __init__(self,x,y,dx,dy):
		self.x = x
		self.y = y
		self.width = 35
		self.height = 35
		self.vel = 15
		self.angle = math.atan2(self.y-dy,self.x-dx)
		self.vel_x = math.cos(self.angle)*self.vel
		self.vel_y = math.sin(self.angle)*self.vel
		self.bullet_image = pygame.image.load(
			os.path.join("Assets","fire.png")).convert_alpha()
	def draw(self,master):
		self.window = master
		self.bullet = pygame.transform.scale(self.bullet_image,(self.width,self.height))
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.window.blit(self.bullet,(self.x,self.y))
	def move(self,dt):
		self.x -= self.vel_x*dt
		self.y -= self.vel_y*dt
