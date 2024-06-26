import tkinter as tk
import numpy as np
from tkinter import messagebox
import os

os.system('cls')

class mainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # main window config
        # self.configure(background='light grey')
        self.resizable(width=False, height=False)
        self.title('game')

        # Constants
        self.turn_indicator_image = tk.PhotoImage(file='ultimate_ttt\yellow_circle.png')
        self.default_button_colour = None   # set within self.add_layout 
        self.win_message = 'player %s wins the game'

        # Variables
        self.player = 'X'
        self.gamestate = np.array([[None for _ in range(9)] for _ in range(9)])   # i = row, j = column (for example, [2][7] is row 2 col 7)
        self.boards_won = {}

        # Adds layout
        self.add_layout()

    # Adds the elements of the game (Header, Frame, Buttons)
    def add_layout(self):
        # creates label for player turn
        self.header = tk.Label(self, text='player %s\'s turn' % self.player, font=('Arial', 18))
        self.header.grid(row=0, column=0)

        # creates frame for buttons
        self.buttonframe = tk.Frame(self, background='black')
        self.buttonframe.grid(row=1, column=0)

        # creates game buttons
        for i in range(9):
            for j in range(9):
                button = tk.Button(self.buttonframe, text='', font=("Arial", 24), height=1, width=3, command=lambda row=i, col=j: self.button_clicked(row, col))
                self.gamestate[i][j] = button

                # Makes the lines between the individual boards. 
                if (j % 10 == 2 or j % 10 == 5) and (i % 10 == 2 or i % 10 == 5):
                    button.grid(row=i, column=j, padx=(0,10), pady=(0,10))
                elif j % 10 == 2 or j % 10 == 5:
                    button.grid(row=i, column=j, padx=(0,10))
                elif i % 10 == 2 or i % 10 == 5:
                    button.grid(row=i, column=j, pady=(0,10))
                else:
                    button.grid(row=i, column=j)
        
        self.default_button_colour = self.gamestate[0][0].cget('background')
        
        # creates reset button
        self.reset = tk.Button(self, fg='red', text='Reset', font=('Arial', 18), command=self.restart)
        self.reset.grid(row=2, column=0)
    
    # When a game button is clicked...
    def button_clicked(self, row, col):
        # Updates button text AND disabled button
        self.gamestate[row][col].config(text=self.player, state='disabled')
        
        # Checking if a board has won everytime a button is clicked
        result, board_row, board_column = self.check_winner_board()
        
        # If a board has won,
        if result:
            self.boards_won[(board_row, board_column)] = self.player
            self.indicate_board_win(board_row, board_column, self.player)
            print(self.boards_won)
            print((board_row, board_column))
            print((board_row, board_column) in self.boards_won)
            
            # messagebox.showinfo(title='title', message='player %s won in board %d %d' % (self.player, board_row, board_column))

        game_result, winner = self.check_winner_game()

        # If someone won the game,
        if game_result:
            messagebox.showinfo(title='WINNER', message=self.win_message % (winner))
            self.disable_game_buttons()
            return

        # Indicates/Sets playable board
        self.disable_game_buttons()
        self.set_playable_board(row, col)
        self.disable_played_buttons()

        # Changes player turn
        self.player = "O" if self.player == "X" else "X"
        self.header.config(text='player %s\'s turn' % self.player)            

    # Checks if any board has won. Returns bool: result, int: row, int: col .
    def check_winner_board(self):
        inv_gamestate = self.gamestate.T

        for row in range(3):
            for col in range(3):
                # Check if that board has won already
                if (row,col) in self.boards_won:
                    continue

                # Check horizontals
                if self.gamestate[3*row][3*col].cget('text') != '' and self.gamestate[3*row][3*col].cget('text') == self.gamestate[3*row][3*col+1].cget('text') == self.gamestate[3*row][3*col+2].cget('text'):
                    return True, row, col
                if self.gamestate[3*row+1][3*col].cget('text') != '' and self.gamestate[3*row+1][3*col].cget('text') == self.gamestate[3*row+1][3*col+1].cget('text') == self.gamestate[3*row+1][3*col+2].cget('text'):
                    return True, row, col
                if self.gamestate[3*row+2][3*col].cget('text') != '' and self.gamestate[3*row+2][3*col].cget('text') == self.gamestate[3*row+2][3*col+1].cget('text') == self.gamestate[3*row+2][3*col+2].cget('text'):
                    return True, row, col
                
                # Checking verticals
                if inv_gamestate[3*col][3*row].cget('text') != '' and inv_gamestate[3*col][3*row].cget('text') == inv_gamestate[3*col][3*row+1].cget('text') == inv_gamestate[3*col][3*row+2].cget('text'):
                    return True, row, col
                if inv_gamestate[3*col+1][3*row].cget('text') != '' and inv_gamestate[3*col+1][3*row].cget('text') == inv_gamestate[3*col+1][3*row+1].cget('text') == inv_gamestate[3*col+1][3*row+2].cget('text'):
                    return True, row, col
                if inv_gamestate[3*col+2][3*row].cget('text') != '' and inv_gamestate[3*col+2][3*row].cget('text') == inv_gamestate[3*col+2][3*row+1].cget('text') == inv_gamestate[3*col+2][3*row+2].cget('text'):
                    return True, row, col
                
                # Checking diagonals
                if self.gamestate[3*row][3*col].cget('text') != '' and self.gamestate[3*row][3*col].cget('text') == self.gamestate[3*row+1][3*col+1].cget('text') == self.gamestate[3*row+2][3*col+2].cget('text'):
                    return True, row, col
                if self.gamestate[3*row][3*col+2].cget('text') != '' and self.gamestate[3*row][3*col+2].cget('text') == self.gamestate[3*row+1][3*col+1].cget('text') == self.gamestate[3*row+2][3*col].cget('text'):
                    return True, row, col
        
        return False, row, col

    # Checks if anyone has won the game.
    def check_winner_game(self):
        # Check horizontals
        if ((0,0) in self.boards_won) and ((0,1) in self.boards_won) and ((0,2) in self.boards_won) and (self.boards_won[(0,0)] == self.boards_won[(0,1)] == self.boards_won[(0,2)]):
            return True, self.boards_won[(0,0)]
        if (1,0) in self.boards_won and (1,1) in self.boards_won and (1,2) in self.boards_won and self.boards_won[(1,0)] == self.boards_won[(1,1)] == self.boards_won[(1,2)]:
            return True, self.boards_won[(1,0)]
        if (2,0) in self.boards_won and (2,1) in self.boards_won and (2,2) in self.boards_won and self.boards_won[(2,0)] == self.boards_won[(2,1)] == self.boards_won[(2,2)]:
            return True, self.boards_won[(2,0)]
        
        # Check verticals
        if ((0,0) in self.boards_won) and ((1,0) in self.boards_won) and ((2,0) in self.boards_won) and (self.boards_won[(0,0)] == self.boards_won[(1,0)] == self.boards_won[(2,0)]):
            return True, self.boards_won[(0,0)]
        if ((0,1) in self.boards_won) and ((1,1) in self.boards_won) and ((2,1) in self.boards_won) and (self.boards_won[(0,1)] == self.boards_won[(1,1)] == self.boards_won[(2,1)]):
            return True, self.boards_won[(0,0)]
        if ((0,2) in self.boards_won) and ((1,2) in self.boards_won) and ((2,2) in self.boards_won) and (self.boards_won[(0,2)] == self.boards_won[(1,2)] == self.boards_won[(2,2)]):
            return True, self.boards_won[(0,0)]
        
        # Check diagonals
        if ((0,0) in self.boards_won) and ((1,1) in self.boards_won) and ((2,2) in self.boards_won) and (self.boards_won[(0,0)] == self.boards_won[(1,1)] == self.boards_won[(2,2)]):
            return True, self.boards_won[(0,0)]
        if ((2,0) in self.boards_won) and ((1,1) in self.boards_won) and ((0,2) in self.boards_won) and (self.boards_won[(2,0)] == self.boards_won[(1,1)] == self.boards_won[(0,2)]):
            return True, self.boards_won[(0,0)]
        
        return False, None

    # Enables the buttons of the playable board.
    def set_playable_board(self, row, col):
        # Finds top corner row of playable board
        if row % 3 == 0:
            board_top_corner_row = 0
        if row % 3 == 1:
            board_top_corner_row = 1
        if row % 3 == 2:
            board_top_corner_row = 2
        
        # Finds top corner column of playable board
        if col % 3 == 0:
            board_top_corner_col = 0
        if col % 3 == 1:
            board_top_corner_col = 1
        if col % 3 == 2:
            board_top_corner_col = 2
        
        # If the next playable board has already been claimed...
        if (board_top_corner_row,board_top_corner_col) in self.boards_won:
            self.enable_game_buttons()

        # If the next playable board has not been claimed...
        else:
            self.enable_board(board_top_corner_row, board_top_corner_col)
        
        # Indicates and disables any claimed boards, by their respective X/O
        for won_board in self.boards_won:
            self.indicate_board_win(won_board[0],won_board[1],self.boards_won[won_board])

    # Places a huge X/O on a board, depending on who won that board.
    def indicate_board_win(self, top_corner_row, top_corner_col, player):
        self.disable_board(top_corner_row, top_corner_col)

        if player == "X":
            self.gamestate[3*top_corner_row][3*top_corner_col].config(bg="black")
            self.gamestate[3*top_corner_row][3*top_corner_col+2].config(bg="black")
            self.gamestate[3*top_corner_row+1][3*top_corner_col+1].config(bg="black")
            self.gamestate[3*top_corner_row+2][3*top_corner_col].config(bg="black")
            self.gamestate[3*top_corner_row+2][3*top_corner_col+2].config(bg="black")
        else:
            self.gamestate[3*top_corner_row][3*top_corner_col+1].config(bg="red")
            self.gamestate[3*top_corner_row+1][3*top_corner_col].config(bg="red")
            self.gamestate[3*top_corner_row+1][3*top_corner_col+2].config(bg="red")
            self.gamestate[3*top_corner_row+2][3*top_corner_col+1].config(bg="red")

    # Enables the buttons of a specific board.
    def enable_board(self, top_corner_row, top_corner_col):
        for i in range(3):
                for j in range(3):
                    self.gamestate[3*top_corner_row+i][3*top_corner_col+j].config(state='active', bg=self.default_button_colour)

    # Disabled the buttons of a specific board.
    def disable_board(self, top_corner_row, top_corner_col):
        for i in range(3):
                for j in range(3):
                    self.gamestate[3*top_corner_row+i][3*top_corner_col+j].config(state='disabled', bg='#bfbfbf')

    # Whole game functions.
    def disable_game_buttons(self):
        for i in range(9):
            for j in range(9):
                self.gamestate[i][j].config(state='disabled', bg='#bfbfbf')

    def enable_game_buttons(self):
        for i in range(9):
            for j in range(9):
                self.gamestate[i][j].config(state='active', bg=self.default_button_colour)

    # Disables buttons which have already been played.
    def disable_played_buttons(self):
        for i in range(9):
            for j in range(9):
                if self.gamestate[i][j].cget('text') != '':
                    self.gamestate[i][j].config(state='disabled')

    def restart(self):
        for i in range(9):
            for j in range(9):
                self.gamestate[i][j].config(text='', state='active', bg=self.default_button_colour)

        # Reset the inself.boards_wonor for which boards have won
        self.boards_won = {}


# Starts the mainWindow loop.
if __name__=="__main__":
    app = mainWindow()
    app.mainloop()

