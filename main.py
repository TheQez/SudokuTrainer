import copy
import tkinter as tk
import tkinter.font as font
from itertools import product
from abc import ABC, abstractmethod
import random

class SudokuGrid:
    def __init__(self, initState=[[None for i in range(0, 9)]for j in range(0, 9)]):
        self.entries = initState
        self.isInLargeMode = [[True for i in range(0, 9)] for j in range(0, 9)]

    # Does not check pencil markings
    def isNoDuplicates(self):
        # Rows
        for i in range(0, 9):
            row = []
            for j in range(0, 9):
                if self.isInLargeMode[i][j]:
                    if self.entries[i][j] in range(1, 10):
                        row.append(self.entries[i][j])
            if len(row) != len(set(row)):
                return False

        # Column
        for i in range(0, 9):
            column = []
            for j in range(0, 9):
                if self.isInLargeMode[j][i]:
                    if self.entries[j][i] in range(1, 10):
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
                            if self.entries[3 * x1 + x2][3 * y1 + y2] in range(1, 10):
                                box.append(self.entries[3 * x1 + x2][3 * y1 + y2])
                if len(box) != len(set(box)):
                    return False

        return True

    def solutions(self):
        currentSudoku = copy.deepcopy(self)
        while True:
            if not currentSudoku.isNoDuplicates():
                return []
            nextSudoku = currentSudoku.getTactic()[0]
            if (nextSudoku.isInLargeMode == currentSudoku.isInLargeMode) and (nextSudoku.entries == currentSudoku.entries):
                break
            currentSudoku = nextSudoku

        return currentSudoku.bruteForce()

    def bruteForce(self, solutionsCutoff=10, randomised=False):
        # Find the next cell not filled
        x, y = None, None
        for i, j in product(range(0, 9), range(0, 9)):
            if not self.isInLargeMode[i][j] or self.entries[i][j] not in range(1, 10):
                x, y = i, j
                break

        # Base case, after sudoku completely filled
        if (x, y) == (None, None):
            if self.isNoDuplicates():
                return [self]
            else:
                return []

        if not self.isInLargeMode[x][y]:
            candidates = list(self.entries[x][y])
        else:
            candidates = [n for n in range(1, 10)]

        if randomised:
            random.shuffle(candidates)

        solutions = []
        for candidate in candidates:
            nextSudoku = copy.deepcopy(self)
            nextSudoku.isInLargeMode[x][y] = True
            nextSudoku.entries[x][y] = candidate
            if nextSudoku.isNoDuplicates():
                solutions += nextSudoku.bruteForce()
            if len(solutions) >= solutionsCutoff:
                break

        return solutions

    def addPenciling(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if (self.isInLargeMode[i][j] and self.entries[i][j] not in range(1, 10)) or (not self.isInLargeMode[i][j] and len(self.entries[i][j]) == 0):
                    self.isInLargeMode[i][j] = False
                    self.entries[i][j] = set([n for n in range(1, 10)])

    def getTactic(self):
        self.addPenciling()
        for tactic in tactics:
            newSudoku, highlightedEntries, removedEntries = tactic.apply(self)
            if newSudoku.entries != self.entries:
                print(tactic.__class__.__name__)
                break
        return newSudoku, highlightedEntries, removedEntries

    def isValid(self):
        sols = self.solutions()
        if len(sols) == 1:
            return True
        else:
            return False

class BackgroundColor():
    DEFAULT = '#FFFFFF'
    LARGESELECTED = '#FFFF00'
    SMALLSELECTED = '#FF00FF'

class TextColor():
    DEFAULT = '#000000'
    REMOVED = '#FF0000'
    USEFUL = '#00FF00'

class SudokuUI:
    selectedCell = (None, None)
    labels = [[0 for i in range(0, 9)] for j in range(0, 9)]
    mainNumberFont = None
    smallNumberFont = None

    currentMode = 'LARGE'
    isShowingTactic = False
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
                if self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]] == int(event.char):
                    self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]] = None
                else:
                    self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]] = int(event.char)
            else:
                self.sudoku.isInLargeMode[self.selectedCell[0]][self.selectedCell[1]] = False
                if type(self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]]) is not set:
                    self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]] = set()
                if int(event.char) not in self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]]:
                    self.sudoku.entries[self.selectedCell[0]][self.selectedCell[1]].add(int(event.char))
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
            if not self.isShowingTactic:
                self.newSudoku, self.highlightedEntries, self.removedEntries = self.sudoku.getTactic()
                if (self.newSudoku.isInLargeMode != self.sudoku.isInLargeMode) or (self.newSudoku.entries != self.sudoku.entries):
                    self.isShowingTactic = True
                else:
                    print('Failed to apply any tactic')
            else:
                self.isShowingTactic = False
                self.sudoku = self.newSudoku

        if event.char == "v":
            print(self.sudoku.isValid())

        self.update()

    def buildLargeLabel(self, master, text, bgcolor, fgcolor):
        label = tk.Label(
            master=master,
            image=pixel,
            text=text,
            width=48,
            height=48,
            borderwidth=0,
            bg=bgcolor,
            fg=fgcolor,
            compound="c",
        )
        label['font'] = self.mainNumberFont
        return label

    def buildSmallLabel(self, master, text, bgcolor, fgcolor):
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
                    bg=bgcolor,
                    fg=fgcolor[x][y],
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
                                    color = BackgroundColor.LARGESELECTED
                                else:
                                    color = BackgroundColor.SMALLSELECTED
                            else:
                                color = BackgroundColor.DEFAULT
                            self.labels[3 * x1 + x2][3 * y1 + y2] = self.buildLargeLabel(smallGrid, currentEntry, color, TextColor.DEFAULT)

                            self.labels[3 * x1 + x2][3 * y1 + y2].grid(row=0, column=0, padx=1, pady=1)

                            clickDetector = self.onClick(3 * x1 + x2, 3 * y1 + y2)
                            self.labels[3 * x1 + x2][3 * y1 + y2].bind('<Button-1>', clickDetector)

                        else:
                            if self.selectedCell[0] == 3*x1 + x2 and self.selectedCell[1] == 3*y1 + y2:
                                if self.currentMode == 'LARGE':
                                    bgcolor = BackgroundColor.LARGESELECTED
                                else:
                                    bgcolor = BackgroundColor.SMALLSELECTED
                            else:
                                bgcolor = BackgroundColor.DEFAULT

                            fgcolor = [[None for i in range(0, 3)] for j in range(0, 3)]
                            for i, j in product(range(0, 3), range(0, 3)):
                                if self.isShowingTactic and (3*i + j + 1) in self.highlightedEntries[3*x1 + x2][3*y1 + y2]:
                                    fgcolor[i][j] = TextColor.USEFUL
                                elif self.isShowingTactic and (3*i + j + 1) in self.removedEntries[3*x1 + x2][3*y1 + y2]:
                                    fgcolor[i][j] = TextColor.REMOVED
                                else:
                                    fgcolor[i][j] = TextColor.DEFAULT

                            self.labels[3*x1 + x2][3*y1 + y2] = self.buildSmallLabel(smallGrid, self.sudoku.entries[3*x1+x2][3*y1+y2], bgcolor, fgcolor)
                            self.labels[3*x1 + x2][3*y1 + y2].grid(row=0, column=0, padx=1, pady=1)
                            clickDetector = self.onClick(3 * x1 + x2, 3 * y1 + y2)
                            self.labels[3 * x1 + x2][3 * y1 + y2].bind('<Button-1>', clickDetector)

from tactics.SudokuTactic import SudokuTactic
from tactics.TrivialPenciling import TrivialPenciling
from tactics.NakedSingle import NakedSingle
from tactics.HiddenSingle import HiddenSingle
from tactics.NakedDouble import NakedDouble

if __name__ == '__main__':
    window = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)

    tactics = []
    tactics.append(TrivialPenciling())
    tactics.append(NakedSingle())
    tactics.append(HiddenSingle())
    tactics.append(NakedDouble())

    sudoku = SudokuUI(window)
    window.mainloop()
