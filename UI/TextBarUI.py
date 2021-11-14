import tkinter as tk


class TextBarUI:
    def __init__(self, window: tk.Tk):
        self.window = window
        #TODO: Do something better than hardcoding the width
        self.textbar = tk.Text(master=self.window, width=64, height=5)
        self.textbar.grid(row=0, column=0)
        self.textbar.configure(state='disabled')

    def changeText(self, text):
        self.textbar.configure(state='normal')
        self.textbar.delete('1.0', tk.END)
        self.textbar.insert(tk.END, text)
        self.textbar.configure(state='disabled')