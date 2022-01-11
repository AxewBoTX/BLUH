import pygame,os,time

class Menu():
	def __init__(self,master,FPS,main_clock,font_,w,h):
		#Main Code
		self.window = master
		self.running = True
		self.FPS = FPS
		self.last_time = time.time()
		self.main_clock = main_clock
		self.font = font_
		self.main_width = w
		self.main_height = h

		#Menu Option Control
		self.on_start,self.on_settings,self.on_about,self.on_exit = True,False,False,False
		self.change = False
		self.setting_pause = False
		self.difficulty_pause = False
		self.can_change = True
		self.music_allowed = False
		self.can_change_ = True

		#Background
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

		#Menu Texts
		self.start_text = self.font.render("start",False,'black')
		self.setting_text = self.font.render("settings",False,'black')
		self.about_text = self.font.render("about",False,'black')
		self.exit_text = self.font.render("exit",False,'black')
		self.black_image = pygame.image.load(os.path.join("Assets","black.png")).convert()
		self.white_image = pygame.image.load(os.path.join("Assets","white.png")).convert()
		self.fullscreen_on = self.font.render("fullscreen on",False,'white')
		self.fullscreen_off = self.font.render("fullscreen off",False,'white')
		self.music_on = self.font.render("music on",False,'white')
		self.music_off = self.font.render("music off",False,'white')
		self.easy = self.font.render("easy",False,'white')
		self.medium = self.font.render("medium",False,'white')
		self.hard = self.font.render("hard",False,'white')
		self.title_font = pygame.font.Font(os.path.join("Assets","font.ttf"),150)
		self.title = self.title_font.render("bluh!",False,'black')

		#Difficulty Options
		self.difficulty = 0

		#Sounds
		self.click = pygame.mixer.Sound(os.path.join("Sounds","switch.wav"))
		self.click.set_volume(0.5)

	#Start Option
	def start(self):
        #Delta Time
		dt = time.time() - self.last_time
		dt *= 60
		self.last_time = time.time()

		#Window Structure
		self.window.fill('white')
		self.current_w = self.window.get_width()
		self.current_h = self.window.get_height()
		self.change = False
		self.world.draw()
		
		#Title
		self.title_rect = pygame.Rect(
			self.current_w/2-self.title.get_width()/2,
			self.current_h/2-self.title.get_height(),
			self.title.get_width(),self.title.get_height())
		self.window.blit(self.title,(self.title_rect.x,self.title_rect.y))
		#Start Button
		self.start_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-330,
			self.start_text.get_width(),self.start_text.get_height())
		self.window.blit(self.start_text,(self.start_rect.x,self.start_rect.y))
		self.outline = pygame.Rect(self.start_rect.x-5,self.start_rect.y,
			self.start_text.get_width()+10,self.start_text.get_height())
		pygame.draw.rect(self.window,'black',self.outline,width=5)
		#Settings Button
		self.settings_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-250,
			self.setting_text.get_width(),self.setting_text.get_height())
		self.window.blit(self.setting_text,(self.settings_rect.x,self.settings_rect.y))
		#About Button
		self.about_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-170,
			self.about_text.get_width(),self.about_text.get_height())
		self.window.blit(self.about_text,(self.about_rect.x,self.about_rect.y))
		#Exit Button
		self.exit_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-90,
			self.exit_text.get_width(),self.exit_text.get_height())
		self.window.blit(self.exit_text,(self.exit_rect.x,self.exit_rect.y))

		#Difficulty Selection
		if self.difficulty_pause == True:
			self.black = pygame.transform.scale(self.black_image,
				(self.current_w,self.current_h))
			self.black.set_colorkey('black')
			self.black.set_alpha(365)
			self.window.blit(self.black,(0,0))
			mouse_pos = pygame.mouse.get_pos()
			clicked = False
			#Easy Button
			self.easy_rect = pygame.Rect(
				self.current_w-self.easy.get_width(),10,
				self.easy.get_width(),self.easy.get_height())
			self.window.blit(self.easy,(self.easy_rect.x,self.easy_rect.y))
			if self.easy_rect.collidepoint(mouse_pos):
				black = pygame.transform.scale(self.black_image,
					(self.easy.get_width(),self.easy.get_height()))
				black.set_colorkey('black')
				black.set_alpha(100)
				self.window.blit(black,(self.easy_rect.x,self.easy_rect.y))
				if pygame.mouse.get_pressed()[0] == 1:
					if clicked == False:
						self.difficulty = 1
						self.difficulty_pause = False
						self.can_change_ = True
						self.change = True
						clicked = True
			if pygame.mouse.get_pressed()[0] == 0:
				clicked = False
			#Medium Button
			self.medium_rect = pygame.Rect(
				self.current_w-self.medium.get_width(),100,
				self.medium.get_width(),self.medium.get_height())
			self.window.blit(self.medium,(self.medium_rect.x,self.medium_rect.y))
			if self.medium_rect.collidepoint(mouse_pos):
				black = pygame.transform.scale(self.black_image, 
					(self.medium_rect.x,self.medium_rect.y))
				black.set_colorkey('black')
				black.set_alpha(100)
				self.window.blit(black,(self.medium_rect.x,self.medium_rect.y))
				if pygame.mouse.get_pressed()[0] == 1:
					if clicked == False:
						self.difficulty = 2
						self.difficulty_pause = False
						self.can_change_ = True
						self.change = True
						clicked = True
			if pygame.mouse.get_pressed()[0] == 0:
				clicked = False
			#Hard Button
			self.hard_rect = pygame.Rect(
				self.current_w-self.hard.get_width(),190,
				self.hard.get_width(),self.hard.get_height())
			self.window.blit(self.hard,(self.hard_rect.x,self.hard_rect.y))
			if self.hard_rect.collidepoint(mouse_pos):
				black = pygame.transform.scale(self.black_image,
					(self.hard_rect.x,self.hard_rect.y))
				black.set_colorkey('black')
				black.set_alpha(100)
				self.window.blit(black,(self.hard_rect.x,self.hard_rect.y))
				if pygame.mouse.get_pressed()[0] == 1:
					if clicked == False:
						self.difficulty = 3
						self.difficulty_pause = False
						self.can_change_ = True
						self.change = True
						clicked = True
			if pygame.mouse.get_pressed()[0] == 0:
				clicked = False

		#Events
		for event in pygame.event.get():
			#Exit Event
			if event.type == pygame.QUIT:
				self.running = False
			#Changing to Settings
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
				if self.can_change_ == True:
					self.on_start = False
					self.on_settings = True
					self.on_about = False
					self.on_exit = False
					self.click.play()
			#Option Select Event
			if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
				self.difficulty_pause = True
				self.can_change_ = False
			if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
				self.difficulty_pause = False
				self.can_change_ = True

		pygame.display.update()
		self.main_clock.tick(self.FPS)

	#Settings Option
	def settings(self):
        #Delta Time
		dt = time.time() - self.last_time
		dt *= 60
		self.last_time = time.time()

		#Window Structure
		self.window.fill('white')
		self.current_w = self.window.get_width()
		self.current_h = self.window.get_height()
		self.world.draw()

		#Title
		self.title_rect = pygame.Rect(
			self.current_w/2-self.title.get_width()/2,
			self.current_h/2-self.title.get_height(),
			self.title.get_width(),self.title.get_height())
		self.window.blit(self.title,(self.title_rect.x,self.title_rect.y))
		#Start Button
		self.start_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-330,
			self.start_text.get_width(),self.start_text.get_height())
		self.window.blit(self.start_text,(self.start_rect.x,self.start_rect.y))
		#Settings Button
		self.settings_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-250,
			self.setting_text.get_width(),self.setting_text.get_height())
		self.window.blit(self.setting_text,(self.settings_rect.x,self.settings_rect.y))
		self.outline = pygame.Rect(self.settings_rect.x-5,self.settings_rect.y,
			self.setting_text.get_width()+10,self.setting_text.get_height())
		pygame.draw.rect(self.window,'black',self.outline,width=5)
		#About Button
		self.about_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-170,
			self.about_text.get_width(),self.about_text.get_height())
		self.window.blit(self.about_text,(self.about_rect.x,self.about_rect.y))
		#Exit Button
		self.exit_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-90,
			self.exit_text.get_width(),self.exit_text.get_height())
		self.window.blit(self.exit_text,(self.exit_rect.x,self.exit_rect.y))

		#Settings Function
		if self.setting_pause == True:
			self.black = pygame.transform.scale(self.black_image,
				(self.current_w,self.current_h))
			self.black.set_colorkey('black')
			self.black.set_alpha(200)
			self.window.blit(self.black,(0,0))
			mouse_pos = pygame.mouse.get_pos()
			clicked = False
			#FullScreen On Button
			self.fullscreen_on_rect = pygame.Rect(
				self.current_w-self.fullscreen_on.get_width(),10,
				self.fullscreen_on.get_width(),self.fullscreen_on.get_height())
			self.window.blit(self.fullscreen_on,(
				self.fullscreen_on_rect.x,self.fullscreen_on_rect.y))
			if self.fullscreen_on_rect.collidepoint(mouse_pos):
				black = pygame.transform.scale(self.black_image,
					(self.fullscreen_on.get_width(),self.fullscreen_on.get_height()))
				black.set_colorkey('black')
				black.set_alpha(100)
				self.window.blit(black,(
					self.fullscreen_on_rect.x,self.fullscreen_on_rect.y))
				if pygame.mouse.get_pressed()[0] == 1:
					if clicked == False:
						pygame.display.set_mode((0,0),pygame.FULLSCREEN)
						clicked = True
			if pygame.mouse.get_pressed()[0] == 0:
				clicked = False
			#FullScreen Off Button
			self.fullscreen_off_rect = pygame.Rect(
				self.current_w-self.fullscreen_off.get_width(),100,
				self.fullscreen_off.get_width(),self.fullscreen_off.get_height())
			self.window.blit(self.fullscreen_off,(
				self.fullscreen_off_rect.x,self.fullscreen_off_rect.y))
			if self.fullscreen_off_rect.collidepoint(mouse_pos):
				black = pygame.transform.scale(self.black_image,
					(self.fullscreen_off.get_width(),self.fullscreen_off.get_height()))
				black.set_colorkey('black')
				black.set_alpha(100)
				self.window.blit(black,(
					self.fullscreen_off_rect.x,self.fullscreen_off_rect.y))
				if pygame.mouse.get_pressed()[0] == 1:
					if clicked == False:
						pygame.display.set_mode((self.main_width,self.main_height))
						clicked = True
			if pygame.mouse.get_pressed()[0] == 0:
				clicked = False
			#Music On Button
			self.music_on_rect = pygame.Rect(
				self.current_w-self.music_on.get_width(),190,
				self.music_on.get_width(),self.music_on.get_height())
			self.window.blit(self.music_on,(self.music_on_rect.x,self.music_on_rect.y))
			if self.music_on_rect.collidepoint(mouse_pos):
				black = pygame.transform.scale(self.black_image,
					(self.music_on.get_width(),self.music_on.get_height()))
				black.set_colorkey('black')
				black.set_alpha(100)
				self.window.blit(black,(self.music_on_rect.x,self.music_on_rect.y))
				if pygame.mouse.get_pressed()[0] == 1:
					if clicked == False:
						self.music_allowed = True
						clicked = True
			if pygame.mouse.get_pressed()[0] == 0:
				clicked = False

			#Music Off Button
			self.music_off_rect = pygame.Rect(
				self.current_w-self.music_off.get_width(),280,
				self.music_off.get_width(),self.music_off.get_height())
			self.window.blit(self.music_off,(self.music_off_rect.x,self.music_off_rect.y))
			if self.music_off_rect.collidepoint(mouse_pos):
				black = pygame.transform.scale(self.black_image,
					(self.music_off.get_width(),self.music_off.get_height()))
				black.set_colorkey('black')
				black.set_alpha(100)
				self.window.blit(black,(self.music_off_rect.x,self.music_off_rect.y))
				if pygame.mouse.get_pressed()[0] == 1:
					if clicked == False:
						self.music_allowed = False
						clicked = True
			if pygame.mouse.get_pressed()[0] == 0:
				clicked = False

		#Events
		for event in pygame.event.get():
			#Exit Event
			if event.type == pygame.QUIT:
				self.running = False
			#Changing To About	
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
				if self.can_change == True:
				    self.on_start = False
				    self.on_settings = False
				    self.on_about = True
				    self.on_exit = False
				    self.click.play()
			#Changing To Start
			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
				if self.can_change == True:
					self.on_start = True
					self.on_settings = False
					self.on_about = False
					self.on_exit = False
					self.click.play()
			#Option Select Event
			if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
				self.setting_pause = True
				self.can_change = False
			if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
				self.setting_pause = False
				self.can_change = True

		pygame.display.update()
		self.main_clock.tick(self.FPS)

	#About Option
	def about(self):
        #Delta Time
		dt = time.time() - self.last_time
		dt *= 60
		self.last_time = time.time()

		#Window Structure
		self.window.fill('white')
		self.current_w = self.window.get_width()
		self.current_h = self.window.get_height()
		self.world.draw()

		#Title
		self.title_rect = pygame.Rect(
			self.current_w/2-self.title.get_width()/2,
			self.current_h/2-self.title.get_height(),
			self.title.get_width(),self.title.get_height())
		self.window.blit(self.title,(self.title_rect.x,self.title_rect.y))
		#Start Button
		self.start_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-330,
			self.start_text.get_width(),self.start_text.get_height())
		self.window.blit(self.start_text,(self.start_rect.x,self.start_rect.y))
		#Settings Button
		self.settings_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-250,
			self.setting_text.get_width(),self.setting_text.get_height())
		self.window.blit(self.setting_text,(self.settings_rect.x,self.settings_rect.y))
		#About Button
		self.about_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-170,
			self.about_text.get_width(),self.about_text.get_height())
		self.window.blit(self.about_text,(self.about_rect.x,self.about_rect.y))
		self.outline = pygame.Rect(self.about_rect.x-5,self.about_rect.y,
			self.about_text.get_width()+10,self.about_text.get_height())
		pygame.draw.rect(self.window,'black',self.outline,width=5)
		#Exit Button
		self.exit_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-90,
			self.exit_text.get_width(),self.exit_text.get_height())
		self.window.blit(self.exit_text,(self.exit_rect.x,self.exit_rect.y))

		#Events
		for event in pygame.event.get():
			#Exit Event
			if event.type == pygame.QUIT:
				self.running = False
			#Changing To Exit
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
				self.on_start = False
				self.on_settings = False
				self.on_about = False
				self.on_exit = True
				self.click.play()
			#Changing to Settings
			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
				self.on_start = False
				self.on_settings = True
				self.on_about = False
				self.on_exit = False
				self.click.play()
			#Option Select Event
			if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
				pygame.display.set_mode((self.main_width,self.main_height))
				os.system(os.path.join("Data","ABOUT.txt"))

		pygame.display.update()
		self.main_clock.tick(self.FPS)

	#Exit Option
	def exit(self):
        #Delta Time
		dt = time.time() - self.last_time
		dt *= 60
		self.last_time = time.time()

		#Window Structure
		self.window.fill('white')
		self.current_w = self.window.get_width()
		self.current_h = self.window.get_height()
		self.world.draw()

		#Title
		self.title_rect = pygame.Rect(
			self.current_w/2-self.title.get_width()/2,
			self.current_h/2-self.title.get_height(),
			self.title.get_width(),self.title.get_height())
		self.window.blit(self.title,(self.title_rect.x,self.title_rect.y))
		#Start Button
		self.start_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-330,
			self.start_text.get_width(),self.start_text.get_height())
		self.window.blit(self.start_text,(self.start_rect.x,self.start_rect.y))
		#Settings Button
		self.settings_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-250,
			self.setting_text.get_width(),self.setting_text.get_height())
		self.window.blit(self.setting_text,(self.settings_rect.x,self.settings_rect.y))
		#About Button
		self.about_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-170,
			self.about_text.get_width(),self.about_text.get_height())
		self.window.blit(self.about_text,(self.about_rect.x,self.about_rect.y))
		#Exit Button
		self.exit_rect = pygame.Rect(
			self.current_w+10-self.current_w,self.current_h-90,
			self.exit_text.get_width(),self.exit_text.get_height())
		self.window.blit(self.exit_text,(self.exit_rect.x,self.exit_rect.y))
		self.outline = pygame.Rect(self.exit_rect.x-5,self.exit_rect.y,
			self.exit_text.get_width()+10,self.exit_text.get_height())
		pygame.draw.rect(self.window,'black',self.outline,width=5)

		#Events
		for event in pygame.event.get():
			#Exit Event
			if event.type == pygame.QUIT:
				self.running = False
			#Changing to About
			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
				self.on_start = False
				self.on_settings = False
				self.on_about = True
				self.on_exit = False
				self.click.play()
			#Option Select Event
			if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
				self.running = False

		pygame.display.update()
		self.main_clock.tick(self.FPS)

	def main_menu(self):
		if self.on_start == True:
			if self.on_settings == False:
				if self.on_about == False:
					if self.on_exit == False:
						self.start()
		if self.on_start == False:
			if self.on_settings == True:
				if self.on_about == False:
					if self.on_exit == False:
						self.settings()
		if self.on_start == False:
			if self.on_settings == False:
				if self.on_about == True:
					if self.on_exit == False:
						self.about()
		if self.on_start == False:
			if self.on_settings == False:
				if self.on_about == False:
					if self.on_exit == True:
						self.exit()