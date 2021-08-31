import copy
import tkinter as tk
import tkinter.font as font
from itertools import product
from abc import ABC, abstractmethod

class SudokuGrid:
    def __init__(self, initState=[[' ' for i in range(0, 9)]for j in range(0, 9)]):
        self.entries = initState
        self.isInLargeMode = [[True for i in range(0, 9)] for j in range(0, 9)]

    # Does not check pencil markings
    def isNoDuplicates(self):
        # Rows
        for i in range(0, 9):
            row = []
            for j in range(0, 9):
                if self.isInLargeMode[i][j]:
                    if self.entries[i][j] in [str(n) for n in range(1, 10)]:
                        row.append(self.entries[i][j])
            if len(row) != len(set(row)):
                return False

        # Column
        for i in range(0, 9):
            column = []
            for j in range(0, 9):
                if self.isInLargeMode[j][i]:
                    if self.entries[j][i] in [str(n) for n in range(1, 10)]:
                        column.append(self.entries[j][i])
            if len(column) != len(set(column)):
                return False

        # Boxes
        for x1 in range(0, 3):
            for y1 in range(0, 3):
                box = []
                for x2 in range(0, 3):
                    for y2 in range(0, 3):
                        if self.isInLargeMode[3 * x1 + x2][3 * y1 + y2]:
                            if self.entries[3 * x1 + x2][3 * y1 + y2] in [str(n) for n in range(1, 10)]:
                                box.append(self.entries[3 * x1 + x2][3 * y1 + y2])
                if len(box) != len(set(box)):
                    return False

        return True

    def solutions(self):
        # Find the next cell not filled
        x, y = None, None
        for i, j in product(range(0, 9), range(0, 9)):
            if not self.isInLargeMode[i][j] or self.entries[i][j] not in [str(n) for n in range(1, 10)]:
                x, y = i, j
                break

        # Base case, after sudoku completely filled
        if (x, y) == (None, None):
            if self.isNoDuplicates():
                return [self]
            else:
                return []

        if not self.isInLargeMode[x][y]:
            candidates = self.entries[x][y]
        else:
            candidates = [str(n) for n in range(1, 10)]

        solutions = []
        for candidate in candidates:
            nextSudoku = copy.deepcopy(self)
            nextSudoku.isInLargeMode[x][y] = True
            nextSudoku.entries[x][y] = str(candidate)
            if nextSudoku.isNoDuplicates():
                solutions += nextSudoku.solutions()

        return solutions

    def addPenciling(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.isInLargeMode[i][j] and self.entries[i][j] not in [str(n) for n in range(1, 10)]:
                    self.isInLargeMode[i][j] = False
                    self.entries[i][j] = [n for n in range(1, 10)]

    def step(self):
        self.addPenciling()
        for tactic in tactics:
            newSudoku = tactic.apply(self)
            if newSudoku.entries != self.entries:
                self.isInLargeMode = newSudoku.isInLargeMode
                self.entries = newSudoku.entries
                print(tactic.__class__.__name__)
                break

class SudokuUI:
    selectedCell = (None, None)
    labels = [[0 for i in range(0, 9)] for j in range(0, 9)]
    mainNumberFont = None
    smallNumberFont = None

    currentMode = 'LARGE'
    def __init__(self, window, sudoku=SudokuGrid()):
        # TODO: Have a real init function
        self.window = window

        self.sudoku = sudoku

        window.bind('<KeyPress>', self.onKeyPress)

        self.mainNumberFont = font.Font(size='30')
        self.smallNumberFont = font.Font(size='10')

        self.update()

    def onClick(self, x, y):
        return lambda event: self.cellClicked(x, y)

    def cellClicked(self, x, y):
        self.selectedCell = (x, y)
        self.update()

    def onKeyPress(self, event):
        if event.char.isdigit() and event.char != '0':
            if self.currentMode == 'LARGE':
                self.sudoku.isInLargeMode[self.selectedCell[0]][self.selectedCell[1]] = True
                if self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]] == event.char:
                    self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]] = None
                else:
                    self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]] = event.char
            else:
                self.sudoku.isInLargeMode[self.selectedCell[0]][self.selectedCell[1]] = False
                if type(self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]]) is not list:
                    self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]] = []
                if int(event.char) not in self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]]:
                    self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]].append(int(event.char))
                else:
                    self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]].remove(int(event.char))

        if event.char == ' ':
            if self.currentMode == 'LARGE':
                self.currentMode = 'SMALL'
            else:
                self.currentMode = 'LARGE'

        if event.char == '0':
            sols = self.sudoku.solutions()
            print(len(sols))
            if len(sols) != 0:
                self.sudoku = sols[0]

        if event.char == "s":
            self.sudoku.step()

        self.update()

    def buildLargeLabel(self, master, text, color):
        label = tk.Label(
            master=master,
            image=pixel,
            text=text,
            width=48,
            height=48,
            borderwidth=0,
            bg=color,
            fg="black",
            compound="c",
        )
        label['font'] = self.mainNumberFont
        return label

    def buildSmallLabel(self, master, text, color):
        labels = [None for i in range(0, 9)]
        miniGrid = tk.Frame(master=master)
        for x in range(0, 3):
            for y in range(0, 3):
                if 3 * x + y + 1 in text:
                    currentEntry = 3 * x + y + 1
                else:
                    currentEntry = " "

                labels[3 * x + y] = tk.Label(
                    master=miniGrid,
                    image=pixel,
                    text=currentEntry,
                    width=16,
                    height=16,
                    borderwidth=0,
                    bg=color,
                    fg="black",
                    compound="c",
                )
                labels[3 * x + y].bindtags((miniGrid,) + labels[3 * x + y].bindtags())

                labels[3 * x + y]['font'] = self.smallNumberFont
                labels[3 * x + y].grid(row=x, column=y)
        return miniGrid

    def update(self):
        for child in self.window.winfo_children():
            child.destroy()

        for x1 in range(0, 3):
            for y1 in range(0, 3):
                mainGrid = tk.Frame(master=window)
                mainGrid.grid(row=x1, column=y1, padx=1, pady=1)
                for x2 in range(0, 3):
                    for y2 in range(0, 3):
                        smallGrid = tk.Frame(master=mainGrid)
                        smallGrid.grid(row=x2, column=y2)

                        if self.sudoku.isInLargeMode[3 * x1 + x2][3 * y1 + y2]:
                            currentEntry = self.sudoku.entries[3 * x1 + x2][3 * y1 + y2]

                            if self.selectedCell[0] == 3*x1 + x2 and self.selectedCell[1] == 3*y1 + y2:
                                if self.currentMode == 'LARGE':
                                    color = '#FFFF00'
                                else:
                                    color = '#FF00FF'
                            else:
                                color = '#FFFFFF'
                            self.labels[3 * x1 + x2][3 * y1 + y2] = self.buildLargeLabel(smallGrid, currentEntry, color)

                            self.labels[3 * x1 + x2][3 * y1 + y2].grid(row=0, column=0, padx=1, pady=1)

                            clickDetector = self.onClick(3 * x1 + x2, 3 * y1 + y2)
                            self.labels[3 * x1 + x2][3 * y1 + y2].bind('<Button-1>', clickDetector)

                        else:
                            if self.selectedCell[0] == 3*x1 + x2 and self.selectedCell[1] == 3*y1 + y2:
                                if self.currentMode == 'LARGE':
                                    color = '#FFFF00'
                                else:
                                    color = '#FF00FF'
                            else:
                                color = '#FFFFFF'
                            self.labels[3*x1 + x2][3*y1 + y2] = self.buildSmallLabel(smallGrid, self.sudoku.entries[3*x1+x2][3*y1+y2], color)
                            self.labels[3*x1 + x2][3*y1 + y2].grid(row=0, column=0, padx=1, pady=1)
                            clickDetector = self.onClick(3 * x1 + x2, 3 * y1 + y2)
                            self.labels[3 * x1 + x2][3 * y1 + y2].bind('<Button-1>', clickDetector)

from tactics.SudokuTactic import SudokuTactic
from tactics.TrivialPenciling import TrivialPenciling
from tactics.NakedSingle import NakedSingle
from tactics.HiddenSingle import HiddenSingle

if __name__ == '__main__':
    window = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)

    tactics = []
    tactics.append(TrivialPenciling())
    tactics.append(NakedSingle())
    tactics.append(HiddenSingle())

    sudoku = SudokuUI(window)
    window.mainloop()
