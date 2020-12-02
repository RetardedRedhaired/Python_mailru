import unittest
import random
import string
from unittest.mock import patch
import tic_tac


class TicTacTest(unittest.TestCase):
    @patch('builtins.print')
    def test_check_winner(self, mock_print):
        game = [None for _ in range(9)]
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

    @patch('builtins.print')
    def test_validate_input(self, mock_print):
        tmp = ''
        game = [None for _ in range(9)]
        for _ in range(random.randint(1, 10)):
            tmp = tmp + random.choice(string.printable)
        self.assertRaises(ValueError, tic_tac.TicTacGame()._validate_input_opt(tmp))
        self.assertRaises(ValueError, tic_tac.TicTacGame()._validate_input_sqr(game, tmp))
        for _ in range(random.randint(1, 10)):
            tmp = tmp + random.choice(string.digits)
        self.assertRaises(ValueError, tic_tac.TicTacGame()._validate_input_opt(tmp))
        self.assertRaises(ValueError, tic_tac.TicTacGame()._validate_input_sqr(game, tmp))
        tmp = random.randint(-10, 0)
        self.assertRaises(ValueError, tic_tac.TicTacGame()._validate_input_opt(tmp))
        self.assertRaises(ValueError, tic_tac.TicTacGame()._validate_input_sqr(game, tmp))
        tmp = random.randint(0,8)
        game[tmp] = True
        self.assertRaises(ValueError, tic_tac.TicTacGame()._validate_input_sqr(game, tmp + 1))


if __name__ == '__main__':
    unittest.main()
