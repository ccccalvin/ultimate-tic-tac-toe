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

        # game variables
        self.player = 'X'
        self.gamestate = np.array([[None for _ in range(9)] for _ in range(9)])   # i = row, j = column (for example, [2][7] is row 2 col 7)
        
        # add layout
        self.add_layout()

    def add_layout(self):
        # creates label for player turn
        self.header = tk.Label(self, text='display player turn', font=('Arial', 18))
        self.header.grid(row=0, column=0)

        # creates frame for buttons
        self.buttonframe = tk.Frame(self, background='red')
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
        
        # creates reset button
        self.reset = tk.Button(self, text='Reset', font=('Arial', 18), command=self.restart)
        self.reset.grid(row=2, column=0)
    
    def button_clicked(self, row, col):
        self.gamestate[row][col].config(text=self.player, state='disabled')
        
        result, board_row, board_column = self.check_winner_board()

        if result:
            messagebox.showinfo(title='title', message='player %s won in board %d %d' % (self.player, board_row, board_column))

        self.player = "O" if self.player == "X" else "X"
        self.header.config(text='player %s\'s turn' % self.player)

        print('clicked')

    def check_winner_board(self):
        inv_gamestate = self.gamestate.T

        for row in range(3):
            for col in range(3):
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
        
        return False, None, None

        
    def disable_board1(self):
        for i in range(3):
                for j in range(3):
                    self.gamestate[i][j].config(state='disabled')

    def restart(self):
        for i in range(9):
            for j in range(9):
                self.gamestate[i][j].config(text='', state='active')


        

        
if __name__=="__main__":
    app = mainWindow()
    app.mainloop()

