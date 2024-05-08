class Game:
    def __init__(self, symbol):
        self.board = [
            " ", " ", " ",
            " ", " ", " ",
            " ", " ", " "
        ]
        self.board_nums = [
            "0", "1", "2",
            "3", "4", "5",
            "6", "7", "8"
        ]
        self.symbol = symbol
        self.opponent_symbol = "X" if symbol == "O" else "O"
        self.is_over = False

    def __print_blanks(self):
        """print a bunch of blank lines to "clear" the terminal"""
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    def __display_boards(self):
        """display a numbered board for reference + the real game board"""
        print(f"\n\t {self.board_nums[0]} | {self.board_nums[1]} | {self.board_nums[2]}"
              f"\t\t\t {self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("\t---+---+---"
              "\t\t\t---+---+---")
        print(f"\t {self.board_nums[3]} | {self.board_nums[4]} | {self.board_nums[5]}"
              f"\t\t\t {self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("\t---+---+---"
              "\t\t\t---+---+---")
        print(f"\t {self.board_nums[6]} | {self.board_nums[7]} | {self.board_nums[8]}"
              f"\t\t\t {self.board[6]} | {self.board[7]} | {self.board[8]}")

    def __display_waiting_message(self):
        """display waiting message"""
        self.__print_blanks()
        print(f"\n\t\t\t\t\t {self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("\t\t\t\t\t---+---+---")
        print(f"\tWaiting for other player... \t {self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("\t\t\t\t\t---+---+---")
        print(f"\t\t\t\t\t {self.board[6]} | {self.board[7]} | {self.board[8]}\n")

    def __display_game_start(self):
        """print game starting message"""
        self.__print_blanks()
        print("\n\n\t\tYOU HAVE JOINED TIC-TAC-TOE!\t\t\t")
        print(" ----------------------------------------------------------------\n")

        print("        ----------------        -------------------------")
        print(f"\t|  You are {self.symbol}s  | \t|  Type 'quit' to quit  |")
        print("        ----------------        -------------------------")

    def __display_game_end(self, add_on=""):
        """print that the game ended, + additional info if needed"""
        self.__print_blanks()
        print(f"\n\t---------- Game ended{add_on} ----------\n\n\n")

    def __display_winner(self, winner):
        """display who won the game"""
        message = "WON" if winner == self.symbol else "LOST"
        self.__print_blanks()
        print("\n\t\t-------------------------")
        print(f"\t\t|\tYOU {message}!!!\t|")
        print("\t\t-------------------------\n\n")

    def __display_turn(self):
        """display that it's your turn + info needed to take turn"""
        self.__print_blanks()
        print("\n\t\t-------------------------")
        print("\t\t|\tYOUR TURN\t|")
        print("\t\t-------------------------")

        self.__display_boards()  # display numbered board + actual game board

    def __mark_space(self, space_number, symbol):
        """marks given space with given symbol"""
        space_number = self.__validate_number(space_number)
        if space_number is not None:
            self.board[space_number] = symbol

    def __get_valid_input(self, user_input):
        """keep prompting user until valid input obtained, then return it"""
        user_input = user_input.strip()

        # check if user wants to quit
        if user_input == "quit":
            return user_input

        # get number that exists in the board
        while user_input not in self.board_nums:
            user_input = input("Invalid space. Please select another numbered space to mark: ")
            if user_input == "quit":
                return user_input

        # get space that is available
        while not self.__is_open_space(user_input):
            user_input = input("Space is taken! Please choose a different spot:  ")
            if user_input == "quit":
                return user_input

        return user_input

    def __validate_number(self, number):
        """checks if given number is a number & returns it as an int"""
        if number.isnumeric():
            return int(number)
        else:
            return

    def __is_open_space(self, space_number):
        """check if given space is taken already"""
        space_number = self.__validate_number(space_number)
        if space_number is not None and self.board[space_number] == " ":
            return True
        else:
            return False

    def __is_board_full(self):
        """check if there are any empty spaces in the board"""
        for space in self.board:
            if space == " ":
                return False
        return True

    def __get_winner(self):
        """check for winning conditions & return winner"""
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)  # diagonals
        ]

        # check if all spaces in combo are same char AND that char isn't blank
        for combo in winning_combinations:
            if ((self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]])
                    and self.board[combo[0]] != " "):
                return self.board[combo[0]]  # return winning symbol

        return None  # return if nobody won

    def start_game(self):
        """print game starting info + prompt user to enter 'start'"""
        self.__display_game_start()

        # wait for user to enter 'start'
        print("\n\t\tType 'start' to start the game")
        user_input = input("\nType here: ").strip()
        while user_input != "start":
            if user_input == "quit":
                print("\n\tYOU ARE NOT ALLOWED TO QUIT BEFORE STARTING THE GAME!!!")
                print("\n\t\tType 'start' to start the game\n")
            user_input = input("Type here: ").strip()

        # X's go first, so O's must wait first
        if self.symbol == "O":
            self.__display_waiting_message()

    def take_turn(self):
        """
        gets input, handles it, displays relevant messages, then returns the input
        """
        self.__display_turn()

        # get input for space to mark
        user_input = input("\nPlease select a numbered space to mark: ")
        user_input = self.__get_valid_input(user_input)

        # mark the selected board space (or display game ending)
        self.handle_input(user_input, self.symbol)

        # show message to wait for turn again if game isn't over
        if not self.is_over:
            self.__display_waiting_message()

        # pass along input so other person can update their game too
        return user_input

    def handle_input(self, user_input, player_symbol=None):
        """
        mark given space
              OR
        display game ending messages + who ended the game
        """
        user_input = user_input.strip()  # remove whitespace
        if player_symbol is not self.symbol:  # update player symbol if none given
            player_symbol = self.opponent_symbol

        self.__mark_space(user_input, player_symbol)

        # check if game has winner
        winner = self.__get_winner()
        if winner is not None:
            self.is_over = True  # update game status
            self.__display_winner(winner)

        # check if game is tied
        elif self.__is_board_full():
            self.is_over = True  # update game status
            self.__display_game_end(" in draw")

        # check if game was quit
        elif user_input == "quit":
            self.is_over = True  # update game status
            # display game ending message depending on who quit
            if player_symbol == self.symbol:  # if game was quit by you
                self.__display_game_end()
            else:
                self.__display_game_end(" by other player")
