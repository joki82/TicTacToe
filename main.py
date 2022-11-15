from tkinter import *
from functools import partial
import random


class Game(Tk):
    """Creating starting window, creating playing board, randomly select who plays first and displays it"""

    def __init__(self):
        super().__init__()
        # Window
        self.title("Tic Tac Toe")
        self.minsize(width=250, height=254)
        self.geometry("+570+160")
        # Lists and variables
        self.button_id = []
        self.row = 1
        self.column = 0
        self.button_pos = None
        self.player_turn = None
        self.all_combos = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.player1_selection = []
        self.player2_selection = []
        self.count_moves = 0
        # Calling methods
        self.create_board()
        self.turn()
        self.display()
        self.who_is_playing()

        self.mainloop()

    def reset_game(self):
        self.row = 1
        self.column = 0
        self.player_turn = None
        self.player1_selection = []
        self.player2_selection = []
        self.count_moves = 0
        for widget in self.field.winfo_children():
            widget.destroy()
        self.field.pack_forget()
        for widget in self.score.winfo_children():
            widget.destroy()
        self.score.pack_forget()
        for widget in self.display_player.winfo_children():
            widget.destroy()
        self.display_player.pack_forget()
        self.button_id = []
        self.button_pos = None
        self.create_board()
        self.turn()
        self.display()
        self.who_is_playing()

    def create_board(self):
        """ Creating buttons 3rows x 3columns and assigning id to each one. Button id added to a button id list.
        For loop creates 9 buttons without text, button command is calling method get_id.
        Created buttons are placed in a grid, row and column set in the class constructor and increased for 1 each
        time for loop runs. Jumps to new row when it reaches last column in a row, else it goes to a next column."""
        self.field = Frame(self)
        self.field.pack()
        for b in range(0, 9):
            button = Button(self.field, text="", width=5, height=4, command=partial(self.play, b))
            button.grid(row=self.row, column=self.column)
            self.button_id.append(button)
            if self.column == 2:
                self.row += 1
                self.column = 0
            else:
                self.column += 1

    def turn(self):
        """Random decision who is playing first O or X """
        self.player_turn = random.randint(0, 1)
        print(self.player_turn)

    # Creates label player and place it on the screen
    def display(self):
        """Creates label player and place it in window"""
        self.display_player = Frame(self)
        self.display_player.pack()
        self.playing = Label(self.display_player, text="")
        self.playing.pack()

    def who_is_playing(self):
        """Updates display which player needs to play O or X"""
        if self.player_turn == 0:
            self.playing.config(text="PLAYER: O")
        else:
            self.playing.config(text="PLAYER: X")

    def play(self, n):
        """When each button is pressed (player places O or X on the board) method receives button number."""
        print(n)
        # Uses button number for index to get button ID from the button_id list.
        self.button_pos = (self.button_id[n])
        # If/else checking whose turn is to play, using even/odd numbers and increasing player_turn for 1.
        if self.player_turn == 0:
            self.button_pos.config(text="O", state="disabled", disabledforeground="red",
                                   highlightbackground="light gray",
                                   highlightthickness=0)
            self.player1_selection.append(n)
            print(self.player1_selection)
            self.check_winner(self.player1_selection, "O")
            self.player_turn = 1
            self.who_is_playing()
        else:
            self.button_pos.config(text="X", state="disabled", disabledforeground="blue",
                                   highlightbackground="light gray",
                                   highlightthickness=0)
            self.player2_selection.append(n)
            print(self.player2_selection)
            self.check_winner(self.player2_selection, "X")
            self.player_turn = 0
            self.who_is_playing()

    def check_winner(self, player_selection, player):
        """Receives all buttons(fields on the board) selected by player and player name (O or X).
        Checks if player has wining combo by comparing player selected buttons with wining combinations.
        Once player has winning combination, buttons are disabled to stop the game and show_score is called. If none of
        two players has winning combination after 9 moves False is sent to show_score, to display draw."""
        for combo in self.all_combos:
            check = all(item in player_selection for item in combo)
            if check:
                print(f"Player {player} is a winner")
                for n in range(0, 9):
                    self.button_pos = (self.button_id[n])
                    self.button_pos.config(state="disabled", highlightbackground="light gray", highlightthickness=0)
                self.show_score(player)
        self.count_moves += 1
        if self.count_moves == 9:
            print("Game over!")
            self.show_score(False)

    def show_score(self, winner):
        """Receiving winning player or False for a draw"""
        self.score = Frame(self)
        self.score.pack()
        reset_button = Button(self.score, text="Reset", width=3, height=3, command=self.reset_game)
        reset_button.pack()
        if not winner:
            self.show_winner = Label(self.score, text=f"It's a draw")
            self.show_winner.pack(side=LEFT, padx=10)
        else:
            self.show_winner = Label(self.score, text=f"Player {winner} is a winner!")
            self.show_winner.pack(side=LEFT, padx=10)


game = Game()
