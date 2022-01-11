import pygame,os,time,math,random
from Data.menu import*
from Data.player import*
from Data.bullet import*
from Data.enemy import*
from Data.health import*

class Game():
	def __init__(self):
		#Main Window
		pygame.init()
		pygame.font.init()
		pygame.mixer.init()
		self.main_width = 1200
		self.main_height = 700
		self.window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.icon = pygame.image.load("icon.ico")
		pygame.display.set_caption("BLUH!")
		pygame.display.set_icon(self.icon)

		#Main Game Assets
		self.FPS = 240
		self.paused = False
		self.running = True
		self.last_time = time.time()
		self.main_clock = pygame.time.Clock()

		#Game State Control Assets
		self.starting = True
		self.shoud_change_start = False
		self.playing = False
		self.schoud_change_palying = False
		self.lost = False
		self.schoud_change_lost = False
		self.paused = False
		self.animation_circle_width = 2100
		self.animate = True
		self.animate_ = False

		#FONTs
		self.main_menu_font = pygame.font.Font(
			os.path.join("Assets","font.ttf"),70)
		self.exit_screen_font = pygame.font.Font(
			os.path.join("Assets","font.ttf"),70)
		self.exit_screen_font_ = pygame.font.Font(
			os.path.join("Assets","font.ttf"),150)
		self.pause_screen_font = pygame.font.Font(
			os.path.join("Assets","font.ttf"),70)
		self.score_font = pygame.font.Font(
			os.path.join("Assets","font.ttf"),40)
		#Main Menu
		self.menu = Menu(self.window,self.FPS,self.main_clock,
			self.main_menu_font,self.main_width,self.main_height)
		#Music
		self.music_track = os.path.join("Music","track.mp3")
		self.music = pygame.mixer.Sound(self.music_track)
		self.music.play(-1)
		self.music.set_volume(0)
		self.difficulty = 0

		#Texts
		self.lost_ = self.exit_screen_font_.render("lost",False,'black')
		self.retry = self.exit_screen_font.render("retry",False,'black')
		self.exit = self.exit_screen_font.render("Exit",False,'black')
		self.resume = self.pause_screen_font.render("resume",False,'white')
		self.exit_ = self.pause_screen_font.render("exit",False,'white')

		#Images
		self.black_image = pygame.image.load(os.path.join("Assets","black.png")).convert()
		self.white_image = pygame.image.load(os.path.join('Assets',"white.png")).convert()
		self.cursor_1 = pygame.image.load(os.path.join("Assets","cross_1.png")).convert_alpha()

		#The Tile-Set World Creation
		#dont worry if you dont know what this code down here mean
		#because neither i did
		self.tile_size = 64
		self.world_data = [
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
		]
		class World():
			def __init__(self,data,tile_size,master):
				self.window = master
				self.tile_size = tile_size
				self.tile_list = []
				ground_tile_path = os.path.join("Assets","floor_tile.png")
				self.ground_tile = pygame.image.load(ground_tile_path).convert()
				row_count = 0
				for row in data:
					col_count = 0
					for tile in row:
						if tile == 1:
							img = pygame.transform.scale(self.ground_tile,(
								self.tile_size,self.tile_size))
							rect = img.get_rect()
							rect.x = col_count*self.tile_size
							rect.y = row_count*self.tile_size
							tile = (img,rect)
							self.tile_list.append(tile)
						col_count += 1
					row_count += 1

			def draw(self):
				for tile in self.tile_list:
					self.window.blit(tile[0],tile[1])

		self.world = World(self.world_data,self.tile_size,self.window)

		#Player
		self.player = Player(590,350)
		self.player_damage_event = pygame.USEREVENT + 0
		pygame.time.set_timer(self.player_damage_event,750)
		self.bullets = []
		self.bullet_contdown = 200
		self.health_spawn_event = pygame.USEREVENT + 3
		pygame.time.set_timer(self.health_spawn_event,7000)
		self.healths = []
		self.score = 0

		#Enemy Spawn Event
		self.spawn_rate = 2000
		self.enemy_event = pygame.USEREVENT + 1
		pygame.time.set_timer(self.enemy_event,self.spawn_rate)
		self.enemies = []

		#Sounds
		self.fire = pygame.mixer.Sound(os.path.join("Sounds","SHOOT.wav"))
		self.enemy_hurt = pygame.mixer.Sound(os.path.join("Sounds","hit.ogg"))
		self.enemy_bullet_sound = pygame.mixer.Sound(os.path.join("Sounds","enemy_shoot.ogg"))

	def main_menu(self):
		pygame.mouse.set_visible(True)
		#Close Event Control
		if self.menu.running == True:
			self.running = True
		elif self.menu.running == False:
			self.running = False
		#Changing the State to playing
		if self.menu.change == True:
			self.starting = False
			self.playing = True
			self.lost = False
		#Music Volume Control
		if self.menu.music_allowed == True:
			self.music.set_volume(0.5)
		elif self.menu.music_allowed == False:
			self.music.set_volume(0)
		#Difficulty
		self.difficulty = self.menu.difficulty
		if self.difficulty == 1:
			self.spawn_rate = 10000
		elif self.difficulty == 2:
			self.spawn_rate == 5000
		elif self.difficulty == 3:
			self.spawn_rate == 500

		self.menu.main_menu()

	def game_window(self):
        #Delta Time
		dt = time.time() - self.last_time
		dt *= 60
		self.last_time = time.time()

		#Window Structure
		self.window.fill('white')
		self.current_w = self.window.get_width()
		self.current_h = self.window.get_height()
		self.world.draw()
		self.player.draw(self.window)
		for bullet in self.bullets:
			bullet.draw(self.window)
		for enemy in self.enemies:
			enemy.draw(self.window,self.player)
		for health in self.healths:
			health.draw(self.window)
			if health.countdown<=0:
				self.healths.remove(health)
			if self.player.rect.colliderect(health.rect):
				if isinstance(health,Health_1):
					self.player.get_health(100)
					self.healths.remove(health)
				elif isinstance(health,Health_2):
					self.player.get_health(150)
					self.healths.remove(health)
				elif isinstance(health,Health_3):
					self.player.get_health(random.randint(50,400))
					self.healths.remove(health)
		self.score_text = self.score_font.render("score "+str(self.score),False,'black')
		self.score_rect = pygame.Rect(10,self.current_h-self.score_text.get_height()-5,
			self.score_text.get_width(),self.score_text.get_height())
		self.window.blit(self.score_text,(self.score_rect.x,self.score_rect.y))

		#When the Game is not paused
		if self.paused == False:
			pygame.mouse.set_visible(False)
			cursor = pygame.transform.scale(self.cursor_1,(60,60))
			cursor_rect = pygame.Rect(pygame.mouse.get_pos()[0],
				pygame.mouse.get_pos()[1],cursor.get_width(),cursor.get_height())
			self.window.blit(cursor,(cursor_rect.x,cursor_rect.y))
			if self.player.current_health<=0:
				self.starting = False
				self.playing = False
				self.lost = True
			#Player Movement
			keypresed = pygame.key.get_pressed()
			#LEFT
			if keypresed[pygame.K_a] or keypresed[pygame.K_LEFT]:
				if self.player.can_left == True:
					self.player.x -= self.player.vel*dt
			#RIGHT
			if keypresed[pygame.K_d] or keypresed[pygame.K_RIGHT]:
				if self.player.can_right == True:
					self.player.x += self.player.vel*dt
			#UP
			if keypresed[pygame.K_w] or keypresed[pygame.K_UP]:
				if self.player.can_up == True:
					self.player.y -= self.player.vel*dt
			#DOWN
			if keypresed[pygame.K_s] or keypresed[pygame.K_DOWN]:
				if self.player.can_down == True:
					self.player.y += self.player.vel*dt

			mouse_pos = pygame.mouse.get_pos()
			#Player Eye Rotation
			if mouse_pos[0] < self.player.x + self.player.width/2:
				self.player.facing_left = True
				self.player.facing_right = False
			if mouse_pos[0] > self.player.x + self.player.width/2:
				self.player.facing_left = False
				self.player.facing_right = True

			#Player Collision With Window Boundaries
			if self.player.x <= 0:
				self.player.can_left = False
			else:
				self.player.can_left = True
			if self.player.x + self.player.width >= self.current_w:	
				self.player.can_right = False
			else:
				self.player.can_right = True
			if self.player.y <= 0:
				self.player.can_up = False
			else:
				self.player.can_up = True
			if self.player.y + self.player.height >= self.current_h:
				self.player.can_down = False
			else:
				self.player.can_down = True

			#Bullet Movement
			self.bullet_contdown -= 5
			for bullet in self.bullets:
				bullet.move(dt)
				if bullet.x <= 0:
					self.bullets.remove(bullet)
				if bullet.x+bullet.width >= self.current_w:
					self.bullets.remove(bullet)
				if bullet.y <= 0:
					self.bullets.remove(bullet)
				if bullet.y+bullet.height >= self.current_h:
					self.bullets.remove(bullet)
				for enemy in self.enemies:
					if bullet.rect.colliderect(enemy.rect):
						if isinstance(enemy,Basic):
							enemy.health -= 25
						elif isinstance(enemy,Shooter):
						    enemy.health -= 20
						self.enemy_hurt.set_volume(0.2)
						self.enemy_hurt.play()
						self.bullets.remove(bullet)
					if enemy.health<=0:
						if isinstance(enemy,Basic):
							self.score += 10
						if isinstance(enemy,Shooter):
							self.score += 50
						self.enemies.remove(enemy)

			#Enemy Movement
			for enemy in self.enemies:
				enemy.move(dt,self.player.x+self.player.width/2,self.player.y+self.player.height/2)
				if enemy.rect.colliderect(self.player.rect):
					if isinstance(enemy,Basic):
						self.player.get_damage(80)
						self.enemies.remove(enemy)
					elif isinstance(enemy,Shooter):
						self.player.get_damage(120)
						self.enemies.remove(enemy)

		#When the Game is paused
		if self.paused == True:
			pygame.mouse.set_visible(True)
			black = pygame.transform.scale(
				self.black_image,(self.current_w,self.current_h))
			black.set_colorkey('black')
			black.set_alpha(150)
			self.window.blit(black,(0,0))
			mouse_pos = pygame.mouse.get_pos()
			pygame.mouse.set_visible(True)
			clicked = False
			#Resume Button
			resume_rect = pygame.Rect(
				self.current_w/2-self.resume.get_width()/2,
				self.current_h/2-45-self.resume.get_height()/2,
				self.resume.get_width(),self.resume.get_height())
			self.window.blit(self.resume,(resume_rect.x,resume_rect.y))
			if resume_rect.collidepoint(mouse_pos):
				black = pygame.transform.scale(self.black_image,
					(self.resume.get_width(),self.resume.get_height()))
				black.set_colorkey('black')
				black.set_alpha(100)
				self.window.blit(black,(resume_rect.x,resume_rect.y))
				if pygame.mouse.get_pressed()[0] == 1:
					if clicked == False:
						self.paused = False
						clicked == True
			if pygame.mouse.get_pressed()[0] == 0:
				clicked = False
			#Exit Button
			exit_rect = pygame.Rect(
				self.current_w/2-self.exit_.get_width()/2,
				self.current_h/2+45-self.exit_.get_height()/2,
				self.exit.get_width(),self.exit_.get_height())
			self.window.blit(self.exit_,(exit_rect.x,exit_rect.y))
			if exit_rect.collidepoint(mouse_pos):
				black = pygame.transform.scale(self.black_image,
					(self.exit_.get_width(),self.exit_.get_height()))
				black.set_colorkey('black')
				black.set_alpha(100)
				self.window.blit(black,(exit_rect.x,exit_rect.y))
				if pygame.mouse.get_pressed()[0] == 1:
					if clicked == False:
						self.paused = False
						self.starting = True
						self.playing = False
						self.lost = False
						self.player.current_health = 1000
						self.bullets = []
						self.enemies = []
						self.healths = []
						self.score = 0
						clicked == True
			if pygame.mouse.get_pressed()[0] == 0:
				clicked = False

		#Events
		for event in pygame.event.get():
			#Quit Event
			if event.type == pygame.QUIT:
				self.running = False
			#Pause Game Events
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				if self.paused == False:
					self.paused = True
				elif self.paused == True:
					self.paused = False
			#Bullet Shoot Event
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.paused == False:
					if self.bullet_contdown<=0:
						self.bullet_contdown = 200
						mouse_pos = pygame.mouse.get_pos()
						mouse_x,mouse_y = mouse_pos[0],mouse_pos[1]
						self.bullets.append(Bullet(
							self.player.x+self.player.width/2,
							self.player.y+self.player.height/2,
							mouse_x,mouse_y))
						self.fire.set_volume(0.8)
						self.fire.play(0)
			#Player Damage With Boundaries
			if event.type == self.player_damage_event:
				if self.difficulty == 3:
					if self.player.x+self.player.width>=self.current_w:
						self.player.get_damage(50)
					elif self.player.x<0:
						self.player.get_damage(50)
					elif self.player.y+self.player.height>self.current_h:
						self.player.get_damage(50)
					elif self.player.y<0:
						self.player.get_damage(50)
			#Enemy Spawn Event
			if event.type == self.enemy_event and self.paused == False:
				#Easy Difficulty
				if self.difficulty == 1:
					enemy_count = random.randint(1,2)
					quadrant = random.randint(1,4)
					if quadrant == 1:
						x = random.randint(0,self.current_w)
						y = random.randint(-500,0)
						if enemy_count == 1:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2:
							self.enemies.append(Shooter(x,y))
					elif quadrant == 2:
						x = random.randint(self.current_w,self.current_w+500)
						y = random.randint(0,self.current_h)
						if enemy_count == 1:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2:
							self.enemies.append(Shooter(x,y))
					elif quadrant == 3:
						x = random.randint(0,self.current_w)
						y = random.randint(self.current_h,self.current_h+500)
						if enemy_count == 1:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2:
							self.enemies.append(Shooter(x,y))
					elif quadrant == 4:
						x = random.randint(-500,0)
						y = random.randint(0,self.current_h)
						if enemy_count == 1:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2:
							self.enemies.append(Shooter(x,y))
				#Medium Difficulty
				elif self.difficulty == 2:
					enemy_count = random.randint(1,3)
					quadrant = random.randint(1,4)
					if quadrant == 1:
						x = random.randint(0,self.current_w)
						y = random.randint(-500,0)
						if enemy_count == 1 or enemy_count == 3:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2:
							self.enemies.append(Shooter(x,y))
					elif quadrant == 2:
						x = random.randint(self.current_w,self.current_w+500)
						y = random.randint(0,self.current_h)
						if enemy_count == 1 or enemy_count == 3:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2:
							self.enemies.append(Shooter(x,y))
					elif quadrant == 3:
						x = random.randint(0,self.current_w)
						y = random.randint(self.current_h,self.current_h+500)
						if enemy_count == 1 or enemy_count == 3:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2:
							self.enemies.append(Shooter(x,y))
					elif quadrant == 4:
						x = random.randint(-500,0)
						y = random.randint(0,self.current_h)
						if enemy_count == 1 or enemy_count == 3:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2:
							self.enemies.append(Shooter(x,y))
				#Hard Difficulty
				elif self.difficulty == 3:
					enemy_count = random.randint(1,4)
					quadrant = random.randint(1,4)
					if quadrant == 1:
						x = random.randint(0,self.current_w)
						y = random.randint(-500,0)
						if enemy_count == 1 or enemy_count == 3:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2 or enemy_count == 4:
							self.enemies.append(Shooter(x,y))
					elif quadrant == 2:
						x = random.randint(self.current_w,self.current_w+500)
						y = random.randint(0,self.current_h)
						if enemy_count == 1 or enemy_count == 3:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2 or enemy_count == 4:
							self.enemies.append(Shooter(x,y))
					elif quadrant == 3:
						x = random.randint(0,self.current_w)
						y = random.randint(self.current_h,self.current_h+500)
						if enemy_count == 1 or enemy_count == 3:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2 or enemy_count == 4:
							self.enemies.append(Shooter(x,y))
					elif quadrant == 4:
						x = random.randint(-500,0)
						y = random.randint(0,self.current_h)
						if enemy_count == 1 or enemy_count == 3:
							self.enemies.append(Basic(x,y))
						elif enemy_count == 2 or enemy_count == 4:
							self.enemies.append(Shooter(x,y))

			#Enemy Bullet Event
			for enemy in self.enemies:
				if isinstance(enemy,Shooter) and self.paused == False:
				    if event.type == enemy.event and enemy.should_move == False:
					    enemy.bullets.append(Enemy_Bullet(enemy.x+enemy.width/2,
						    enemy.y+enemy.height/2,self.player.x+self.player.width/2,
						    self.player.y+self.player.height/2))
					    self.enemy_bullet_sound.set_volume(0.5)
					    self.enemy_bullet_sound.play()
			#Player Health Event
			if event.type == self.health_spawn_event:
				health_count = random.randint(1,4)
				if health_count == 1 or health_count == 4:
					x = random.randint(100,self.current_w-100)
					y = random.randint(100,self.current_h-100)
					self.healths.append(Health_1(x,y))
				if health_count == 2:
					x = random.randint(100,self.current_w-100)
					y = random.randint(100,self.current_h-100)
					self.healths.append(Health_2(x,y))
				if health_count == 3:
					x = random.randint(100,self.current_w-100)
					y = random.randint(100,self.current_h-100)
					self.healths.append(Health_3(x,y))

		#Updating the Display and Ticking the FPS
		pygame.display.update()
		self.main_clock.tick(self.FPS)

	def lost_game(self):
		pygame.mouse.set_visible(True)
		#Delta Time
		dt = time.time() - self.last_time
		dt *= 60
		self.last_time = time.time()

		#Window Structure
		self.window.fill('red')
		self.current_w = self.window.get_width()
		self.current_h = self.window.get_height()
		#Lost Display
		self.lost_rect = pygame.Rect(
			self.current_w/2-self.lost_.get_width()/2,self.current_h-550,
			self.lost_.get_width(),self.lost_.get_height())
		self.window.blit(self.lost_,(self.lost_rect.x,self.lost_rect.y))
		mouse_pos = pygame.mouse.get_pos()
		clicked = False
		#Retry Button
		self.retry_rect = pygame.Rect(
			self.current_w/2-self.retry.get_width()/2,self.current_h-310,
			self.retry.get_width(),self.retry.get_height())
		self.window.blit(self.retry,(self.retry_rect.x,self.retry_rect.y))
		if self.retry_rect.collidepoint(mouse_pos):
			black = pygame.transform.scale(self.black_image,
				(self.retry.get_width(),self.retry.get_height()))
			black.set_colorkey('black')
			black.set_alpha(100)
			self.window.blit(black,(self.retry_rect.x,self.retry_rect.y))
			if pygame.mouse.get_pressed()[0] == 1:
				if clicked == False:
					self.starting = False
					self.playing = True
					self.lost = False
					self.player.current_health = 1000
					self.enemies = []
					self.healths = []
					self.bullets = []
					self.score = 0
					clicked = False

		if pygame.mouse.get_pressed()[0] == 0:
			clicked = False
		#Score Display
		score_rect = pygame.Rect(self.current_w/2-self.score_text.get_width()/2,
			self.current_h-340-self.score_text.get_height()/2,self.score_text.get_width(),
			self.score_text.get_height())
		self.window.blit(self.score_text,(score_rect.x,score_rect.y))
		#Exit Button
		self.exit_rect = pygame.Rect(
			self.current_w/2-self.exit.get_width()/2,self.current_h-220,
			self.exit.get_width(),self.exit.get_height())
		self.window.blit(self.exit,(self.exit_rect.x,self.exit_rect.y))
		if self.exit_rect.collidepoint(mouse_pos):
			black = pygame.transform.scale(self.black_image,
				(self.exit.get_width(),self.exit.get_height()))
			black.set_colorkey('black')
			black.set_alpha(100)
			self.window.blit(black,(self.exit_rect.x,self.exit_rect.y))
			if pygame.mouse.get_pressed()[0] == 1:
				if clicked == False:
					self.running = False
					clicked = False
		if pygame.mouse.get_pressed()[0] == 0:
			clicked = False

		#Events
		for event in pygame.event.get():
			#Quit Event
			if event.type == pygame.QUIT:
				self.running = False

		#Updating the Display and Ticking the FPS
		pygame.display.update()
		self.main_clock.tick(self.FPS)
