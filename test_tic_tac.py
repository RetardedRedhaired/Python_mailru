import unittest
import random
import string
import tic_tac


class TicTacTest(unittest.TestCase):
	def test_check_winner(self):
		game = []
		for _ in range(9):
			game.append(None)
		for i in range(3):
			game[i*3] = game[i*3+1] = game[i*3+2] = True
			self.assertFalse(tic_tac.TicTacGame()._check_winner(game))
			game[i*3] = game[i*3+1] = game[i*3+2] = None
			game[i] = game[i+3] = game[i+6] = True
			self.assertFalse(tic_tac.TicTacGame()._check_winner(game))
			game[i] = game[i+3] = game[i+6] = None
		game[0] = game[4] = game[8] = True
		self.assertFalse(tic_tac.TicTacGame()._check_winner(game))
		game[0] = game[4] = game[8] = None
		game[2] = game[4] = game[6] = True
		self.assertFalse(tic_tac.TicTacGame()._check_winner(game))
	
	def test_validate_input(self):
		tmp = ''
		for _ in range(random.randint(1, 10)):
			tmp = tmp + random.choice(string.printable)
		self.assertRaises(ValueError, tic_tac.TicTacGame()._validate_input(tmp))
		self.assertTrue(tic_tac.TicTacGame()._validate_input(random.randint(1, 100)))


if __name__ == '__main__':
	unittest.main()
