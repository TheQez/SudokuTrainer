import tkinter as tk

from UI.SudokuUI import SudokuUI as SudokuUI
from UI.TextBarUI import TextBarUI as TextBarUI
from UI.TacticVisualiserUI import TacticVisualiserUI as TacticVisualiserUI

if __name__ == '__main__':
    window = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)

    layout1 = tk.Frame(master=window)

    sudokuFrame = tk.Frame(master=layout1)
    textbarFrame = tk.Frame(master=layout1)
    visualiserFrame = tk.Frame(master=window)

    textbar = TextBarUI(textbarFrame)
    sudoku = SudokuUI(sudokuFrame, textbar)
    visualiser = TacticVisualiserUI(visualiserFrame)

    window.bind('<KeyPress>', sudoku.onKeyPress)

    sudokuFrame.grid(row=0, column=0)
    textbarFrame.grid(row=1, column=0)
    layout1.grid(row=0, column=0)
    visualiserFrame.grid(row=0, column=1)

    window.mainloop()
