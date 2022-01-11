import pygame,os

class Health_1():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.width,self.height = 60,60
		self.image = pygame.image.load(os.path.join("Assets","health_1.png")).convert_alpha()
		self.sound = pygame.mixer.Sound(os.path.join("Sounds","health.ogg"))
		self.countdown = 3000
	def draw(self,master):
		self.window = master
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.health = pygame.transform.scale(self.image,(
			self.width,self.height))
		self.window.blit(self.health,(self.x,self.y))
		self.countdown -= 5
class Health_2():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.width,self.height = 50,86
		self.image = pygame.image.load(os.path.join("Assets","health_2.png")).convert_alpha()
		self.sound = pygame.mixer.Sound(os.path.join("Sounds","health.ogg"))
		self.countdown = 3000
	def draw(self,master):
		self.window = master
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.health = pygame.transform.scale(self.image,(
			self.width,self.height))
		self.window.blit(self.health,(self.x,self.y))
		self.countdown -= 5
class Health_3():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.width,self.height = 60,60
		self.image = pygame.image.load(os.path.join("Assets","health_3.png")).convert_alpha()
		self.sound = pygame.mixer.Sound(os.path.join("Sounds","health.ogg"))
		self.countdown = 3000
	def draw(self,master):
		self.window = master
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.health = pygame.transform.scale(self.image,(
			self.width,self.height))
		self.window.blit(self.health,(self.x,self.y))
		self.countdown -= 5