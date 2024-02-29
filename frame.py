import tkinter as tk

class Game(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="red")
        self.parent = parent
        self.add_buttons()

    def add_buttons(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self, text='', font=("Arial", 24), height=1, width=3, pady=5, padx=5)
                button.grid(row=i, column=j, sticky='ew')

    def test(self):
        a = self.parent
        print(a)
