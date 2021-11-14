import tkinter as tk

from UI.SudokuUI import SudokuUI as SudokuUI
from UI.TextBarUI import TextBarUI as TextBarUI

if __name__ == '__main__':
    window = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)

    sudokuFrame = tk.Frame(master=window)
    textbarFrame = tk.Frame(master=window)
    textbar = TextBarUI(textbarFrame)
    sudoku = SudokuUI(sudokuFrame, textbar)

    window.bind('<KeyPress>', sudoku.onKeyPress)

    sudokuFrame.grid(row=0, column=0)
    textbarFrame.grid(row=1, column=0)
    window.mainloop()
