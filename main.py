import tkinter as tk
from tkinter import messagebox
from frame import Game
import os

os.system('cls')

class mainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # main window config
        # self.configure(background='light grey')
        self.resizable(width=False, height=False)
        self.title('game')

        # game variables
        self.player = 'X'
        
        # adds layout
        self.add_layout()

    def add_layout(self):
        # label for player turn
        self.header = tk.Label(self, text='display player turn', font=('Arial', 18))
        self.header.pack()

        # adding individual game boards
        self.buttonframe = tk.Frame(self, background='black')
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=1)
        self.buttonframe.pack(fill='both')

        for i in range(3):
            for j in range(3):
                game = Game(self.buttonframe)
                game.grid(row=i, column=j, padx=20, pady=20)
        
        # reset button
        self.reset = tk.Button(self, text='Reset', font=('Arial', 18))
        self.reset.pack()
    
    def button_clicked(self):
        print('hello')

        
if __name__=="__main__":
    app = mainWindow()
    app.mainloop()

    