from random import randint


class TicTacGame:

	def __init__(self):
		pass
	
	def _print_square(self, tmp, game):
	"""
	Метод получает на вход данные об игровом поле и номер клетки, в которую
	игрок решил походить. Результатом являяется вывод содержимого клетки.
	"""
		if game[tmp] is True:
			print(" X ", end = "")
		elif game[tmp] is False:
			print(" O ", end = "")
		else:
			print(f" {tmp+1} ", end = "")
		
	def _show_board(self, game):
	"""
	Метод получает на вход данные об игровом поле и печатает границы поля.
	Вызывает метод _print_square для заполнения клеток на поле.
	"""
		for tmp in range(9):
			self._print_square(tmp, game)
			if tmp == 2 or tmp == 5:
				print('\n'"═══╬═══╬═══")
				continue
			if tmp == 8:
				print('\n')
				continue
			print("║", end = "")	
		
	def _validate_input(self) -> int:
	"""
	Проверяем, что значения, введенные пользователем являются целыми числами
	"""
		while True:
			try:
				tmp = input()
				number = int(tmp)
			except ValueError:
				print("Please enter valid integer number: ", end = "")
			else:
				return number
		
	def _game_against_player(self):
	"""
	Основной метод воспроизводящий игру. 
	"""
		game = []
		for _ in range(9):
			game.append(None)
		tmp = randint(1, 2)
		if tmp == 1:
			print("You are playing by crosses X. First move is your's")
		else:
			print("You are playing by noughts O. Your's opponent moves first")
		counter = 0
		while self._check_winner(game):
			self._show_board(game)
			while True:
				print("Enter the number of the square: ", end="")
				sqr = self._validate_input()
				if sqr <= 0 or sqr > 9:
					print("Please enter number from 1 to 9")
					continue
				if game[sqr-1] != None:
					print("This sqruare is already occupied, choose another one")
					continue
				break
			if counter % 2 == 0:
				game[sqr-1] = True
			else:
				game[sqr-1] = False
			counter += 1
			if counter == 9:
				if not self._check_winner(game):
					break
				self._show_board(game)
				print("It's a draw!")
				break
	
	def start_game(self):
	"""
	Метод выводящий UI для выбора режима игры
	"""
		print("Do you wish to play against:\n1. Bot\n2. Another player\nYour choice: ", end="")
		while True:
			choice = self.validate_input()
			if choice == 1:
				print("This option isn't ready yet")
				break
			elif choice == 2:
				self._game_against_player()
			else:
  				print("Please enter 1 or 2: ", end = "")
		
	def _check_winner(self, game) -> bool:
	"""
	Метод проверки победы одного из игроков. Получает на вход данные об
	игровом поле, возвращает логические выражения False в случае победы
	и True в случае продолжения игры.
	"""
		for i in range(3):
			if game[i*3] == game[i*3+1] == game[i*3+2] != None or game[i] == game[i+3] == game[i+6] != None:
				self._show_board(game)
				print("Winner!")
				return False
		if game[0] == game[4] == game[8] != None or game[2] == game[4] == game[6] != None:
			self._show_board(game)
			print("Winner!")
			return False
		return True
		

if __name__ == '__main__':
	game = TicTacGame()
	game.start_game()
