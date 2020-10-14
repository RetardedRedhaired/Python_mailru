from random import randint


class TicTacGame():
    def _print_square(self, tmp, game):
        """
        Метод получает на вход данные об игровом поле и номер клетки, в которую
        игрок решил походить. Результатом являяется вывод содержимого клетки.
        """
        if game[tmp] is True:
            print(" X ", end="")
        elif game[tmp] is False:
            print(" O ", end="")
        else:
            print(f" {tmp+1} ", end="")

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
            print("║", end="")

    def _validate_input_opt(self, inp) -> int:
        """
        Проверяем, что значения, введенные пользователем являются целыми
        """
        try:
            number = int(inp)
        except ValueError:
            print("You entered not an integer number", )
        else:
            if number > 0 and number <= 3:
                return number
            print("Your number should be 1, 2 or 3")
            
    def _validate_input_sqr(self, game, inp) -> int:
        """
        Проверяем, что значения, введенные пользователем являются целыми
        """
        try:
            number = int(inp)
        except ValueError:
            print("You entered not an integer number", )
        else:
            if number > 0 and number <= 9:
                if game[number-1] is None:
                    return number
                print("This sqruare is occupied, choose another one")
            print("Your number is not in [1, 9]")

    def _game_against_player(self):
        """
        Основной метод воспроизводящий игру.
        """
        game = [None for _ in range(9)]
        tmp = randint(1, 2)
        if tmp == 1:
            print("You are playing by crosses X. First move is your's")
        else:
            print("You are playing by noughts O. Your's opponent moves first")
        counter = 0
        while self._check_winner(game):
            sqr = None
            self._show_board(game)
            while sqr is None:
                print("Enter the number of the square: ", end="")
                tmp = input()
                sqr = self._validate_input_sqr(game, tmp)
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
        while True:
            choice = None
            while choice is None:
                print("Do you wish to play against:\n1. Bot")
                print("2. Another player\n3. Exit\nYour choice: ", end="")
                tmp = input()
                choice = self._validate_input_opt(tmp)
            if choice == 1:
                print("This option isn't ready yet")
                break
            elif choice == 2:
                self._game_against_player()
            else:
                break

    @staticmethod
    def _win_variants(game) -> bool:
        """
        Метод содержащий варианты победы.
        """
        for i in range(3):
            if game[i*3] == game[i*3+1] == game[i*3+2] and game[i*3] is not None:
                return True
            if game[i] == game[i+3] == game[i+6] and game[i] is not None:
                return True
        if game[0] == game[4] == game[8] and game[0] is not None:
            return True
        if game[2] == game[4] == game[6] and game[2] is not None:
            return True
        return False

    def _check_winner(self, game) -> bool:
        """
        Метод проверки победы одного из игроков. Получает на вход данные об
        игровом поле, печатает поле и возвращает логические выражения False
        в случае победы и True в случае продолжения игры.
        """
        if self._win_variants(game):
            self._show_board(game)
            print("Winner!")
            return False
        return True


if __name__ == '__main__':
    game = TicTacGame()
    game.start_game()
