import tkinter as tk
from tkinter import messagebox
import os

os.system('cls')

class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # self.root = tk.Tk()
        # self.geometry('500x500')
        self.title('game')

        self.player = 'X'
        self.gamestate = [[None, None, None], 
                          [None, None, None], 
                          [None, None, None]]

        self.add_layout()
        self.mainloop()

    def add_layout(self):
        # displays player turn
        self.header = tk.Label(self, text='display player turn', font=('Arial', 18))
        self.header.pack(padx=20, pady=20)

        # main game buttons
        self.buttonframe = tk.Frame(self)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=1)
        self.buttonframe.pack(fill='both')
        
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.buttonframe, text='', font=("Arial", 24), height=3, width=8, pady=5, padx=5, command=lambda row=i, col=j: self.is_clicked(row, col))
                self.gamestate[i][j] = button
                button.grid(row=i, column=j, sticky='ew')

        # restart button
        self.testbutton = tk.Button(self, text='reset', font=('Arial', 18), command=self.restart)
        self.testbutton.pack()

    def is_clicked(self, row, col):
        self.gamestate[row][col].config(text=self.player, state='disabled')
        

        if self.check_winner():
            messagebox.showinfo(title='title', message='player %s won' % self.player)

            for i in range(3):
                for j in range(3):
                    self.gamestate[i][j].config(state='disabled')

        elif self.check_draw():
            messagebox.showinfo(title='title', message='draw (ya\'ll too smart)')


        self.player = "O" if self.player == "X" else "X"
        self.header.config(text='player %s\'s turn' % self.player)
        
    def check_winner(self):
        x = tuple(zip(self.gamestate[0], self.gamestate[1], self.gamestate[2]))
        #print(tuple(gamestate_cols))

        # Check horizontals
        if self.gamestate[0][0].cget('text') != '' and all(cell.cget('text') == self.gamestate[0][0].cget('text') for cell in self.gamestate[0]):
            return True
        if self.gamestate[1][0].cget('text') != '' and all(cell.cget('text') == self.gamestate[1][0].cget('text') for cell in self.gamestate[1]):
            return True
        if self.gamestate[2][0].cget('text') != '' and all(cell.cget('text') == self.gamestate[2][0].cget('text') for cell in self.gamestate[2]):
            return True
        
        # Check vertical
        if self.gamestate[0][0].cget('text') != '' and all(cell.cget('text') == self.gamestate[0][0].cget('text') for cell in x[0]):
            return True
        if self.gamestate[0][1].cget('text') != '' and all(cell.cget('text') == self.gamestate[0][1].cget('text') for cell in x[1]):
            return True
        if self.gamestate[0][2].cget('text') != '' and all(cell.cget('text') == self.gamestate[0][2].cget('text') for cell in x[2]):
            return True

        # Check diagonals
        if self.gamestate[0][0].cget('text') != '' and self.gamestate[0][0].cget('text') == self.gamestate[1][1].cget('text') == self.gamestate[2][2].cget('text'):
            return True
        if self.gamestate[0][2].cget('text') != '' and self.gamestate[0][2].cget('text') == self.gamestate[1][1].cget('text') == self.gamestate[2][0].cget('text'):
            return True
        
        return False
    
    def check_draw(self):
        for i in range(3):
            for j in range(3):
                if self.gamestate[i][j].cget('text') == '':
                    return False
                
        return True
    
    def restart(self):
        for i in range(3):
            for j in range(3):
                self.gamestate[i][j].config(text='', state='active')


mainWindow()