import tkinter as tk
import numpy as np
from tkinter import messagebox
from frame import Game
import os

os.system('cls')

class mainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # main window config
        # self.configure(background='light grey')
        # self.resizable(width=False, height=False)
        self.title('game')

        # Constants
        self.turn_indicator_image = tk.PhotoImage(file='ultimate_ttt\yellow_circle.png')
        self.default_button_colour = None   # set within self.add_layout 

        # Variables
        self.player = 'X'
        self.gamestate = np.array([[None for _ in range(9)] for _ in range(9)])   # i = row, j = column (for example, [2][7] is row 2 col 7)
        self.boards_won = []

        # Adds layout
        self.add_layout()

    def add_layout(self):
        # creates label for player turn
        self.header = tk.Label(self, text='display player turn', font=('Arial', 18))
        self.header.grid(row=0, column=0)

        # creates frame for buttons
        self.buttonframe = tk.Frame(self)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=1)
        self.buttonframe.grid(row=1, column=0)

        # creates game buttons
        for i in range(9):
            for j in range(9):
                button = tk.Button(self.buttonframe, text='', font=("Arial", 24), height=1, width=3, pady=5, padx=5, command=lambda row=i, col=j: self.button_clicked(row, col))
                self.gamestate[i][j] = button
                button.grid(row=i, column=j, sticky='ew')
        
        self.default_button_colour = self.gamestate[0][0].cget('background')
        
        # creates reset button
        self.reset = tk.Button(self, text='Reset', font=('Arial', 18), command=self.restart)
        self.reset.grid(row=2, column=0)
    
    def button_clicked(self, row, col):
        # Updates button text AND disabled button
        self.gamestate[row][col].config(text=self.player, state='disabled')
        
        # Checking if a board has won everytime a button is clicked
        result, board_row, board_column = self.check_winner_board()

        # If a board has won,
        if result:
            self.boards_won.append([board_row, board_column])
            self.indicate_board_win(board_row, board_column)
            self.disable_board(board_row, board_column)
            
            messagebox.showinfo(title='title', message='player %s won in board %d %d' % (self.player, board_row, board_column))

        # Updates player turn label
        self.player = "O" if self.player == "X" else "X"
        self.header.config(text='player %s\'s turn' % self.player)

        # Indicates/sets playable board
        self.disable_game_buttons()
        self.set_playable_board(row, col)

        # print('clicked')

    def check_winner_board(self):
        inv_gamestate = self.gamestate.T

        for row in range(3):
            for col in range(3):
                # Check if that board has won already
                if [row,col] in self.boards_won:
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
        
        self.enable_board(board_top_corner_row, board_top_corner_col)

    def enable_board(self, top_corner_row, top_corner_col):
        for i in range(3):
                for j in range(3):
                    self.gamestate[3*top_corner_row+i][3*top_corner_col+j].config(state='active', bg=self.default_button_colour)

    def indicate_board_win(self, top_corner_row, top_corner_col):
        if self.player == "X":
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

    def disable_board(self, top_corner_row, top_corner_col):
        for i in range(3):
                for j in range(3):
                    self.gamestate[3*top_corner_row+i][3*top_corner_col+j].config(state='disabled')
    
    def disable_game_buttons(self):
        for i in range(9):
            for j in range(9):
                self.gamestate[i][j].config(state='disabled', bg='light grey')

    def restart(self):
        for i in range(9):
            for j in range(9):
                self.gamestate[i][j].config(text='', state='active', bg=self.default_button_colour)

        # Reset the indictor for which boards have won
        self.boards_won = []


if __name__=="__main__":
    app = mainWindow()
    app.mainloop()

