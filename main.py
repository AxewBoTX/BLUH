from game import*

#The Game
game = Game()

while game.running == True:
	#Main Menu Screen
	if game.starting == True:
		if game.playing == False:
			if game.lost == False:
				game.main_menu()
	#Actual Game
	if game.starting == False:
		if game.playing == True:
			if game.lost == False:
				game.game_window()
	#Lost Screen
	if game.starting == False:
		if game.playing == False:
			if game.lost == True:
				game.lost_game()