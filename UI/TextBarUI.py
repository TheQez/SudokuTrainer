import tkinter as tk


class TextBarUI:
    #Build a text box that displays the last few lines of text sent to it.
    def __init__(self, window: tk.Tk):
        self.window = window
        self.textbar = tk.Text(master=self.window, width=64, height=5)
        self.textbar.grid(row=0, column=0)

    def changeText(self, text):
        self.textbar.configure(state='normal')
        self.textbar.delete('1.0', tk.END)
        self.textbar.insert(tk.END, text)
        self.textbar.configure(state='disabled')