import tkinter as tk

from UI.SudokuUI import SudokuUI as SudokuUI

if __name__ == '__main__':
    window = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)

    sudoku = SudokuUI(window)
    window.mainloop()
