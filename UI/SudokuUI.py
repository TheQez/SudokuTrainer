from SudokuGrid import SudokuGrid as SudokuGrid
import tkinter as tk
import tkinter.font as font
from itertools import product
import GenerateSudoku

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
    def __init__(self, window: tk.Tk, sudoku: SudokuGrid=SudokuGrid()):
        # TODO: Have a real init function
        self.window = window
        self.pixel = tk.PhotoImage(width=1, height=1)
        self.sudoku = sudoku

        window.bind('<KeyPress>', self.onKeyPress)

        self.mainNumberFont = font.Font(size='30')
        self.smallNumberFont = font.Font(size='10')

        self.update()

    def onClick(self, x: int, y: int):
        return lambda event: self.cellClicked(x, y)

    def cellClicked(self, x: int, y: int):
        self.selectedCell = (x, y)
        self.update()

    def onKeyPress(self, event: tk.Event):
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
            sols = self.sudoku.solutions(solutionsCutoff=10, randomised=True)
            print(len(sols))
            if len(sols) != 0:
                self.sudoku = sols[0]

        if event.char == "s":
            if not self.isShowingTactic:
                self.newSudoku, self.highlightedEntries, self.removedEntries, tactic = self.sudoku.getTactic()
                if (self.newSudoku.isInLargeMode != self.sudoku.isInLargeMode) or (self.newSudoku.entries != self.sudoku.entries):
                    print(tactic.__name__)
                    self.isShowingTactic = True
                else:
                    print('Failed to apply any tactic')
            else:
                self.isShowingTactic = False
                self.sudoku = self.newSudoku

        if event.char == "v":
            print(self.sudoku.isValid())

        if event.char == "f":
            self.sudoku = GenerateSudoku.generateSudoku()

        self.update()

    def buildLargeLabel(self, master: tk.Frame, text, bgcolor: str, fgcolor: str) -> tk.Label:
        label = tk.Label(
            master=master,
            image=self.pixel,
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

    def buildSmallLabel(self, master: tk.Frame, text, bgcolor: str, fgcolor: str) -> tk.Frame:
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
                    image=self.pixel,
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
                mainGrid = tk.Frame(master=self.window)
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