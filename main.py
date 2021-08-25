import tkinter as tk
import tkinter.font as font



class SudokuGrid:
    selectedCell = (None, None)
    isInLargeMode = [[True for i in range(0, 9)] for j in range(0, 9)]
    labels = [[0 for i in range(0, 9)] for j in range(0, 9)]
    entries = [[' ' for i in range(0, 9)] for j in range(0, 9)]
    mainNumberFont = None
    smallNumberFont = None

    currentMode = 'LARGE'
    def __init__(self, window):
        # TODO: Have a real init function
        self.window = window

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
                self.isInLargeMode[self.selectedCell[0]][self.selectedCell[1]] = True
                if self.entries[self.selectedCell[0]][self.selectedCell[1]] == event.char:
                    self.entries[self.selectedCell[0]][self.selectedCell[1]] = None
                else:
                    self.entries[self.selectedCell[0]][self.selectedCell[1]] = event.char
            else:
                self.isInLargeMode[self.selectedCell[0]][self.selectedCell[1]] = False
                if type(self.entries[self.selectedCell[0]][self.selectedCell[1]]) is not list:
                    self.entries[self.selectedCell[0]][self.selectedCell[1]] = []
                if int(event.char) not in self.entries[self.selectedCell[0]][self.selectedCell[1]]:
                    self.entries[self.selectedCell[0]][self.selectedCell[1]].append(int(event.char))
                else:
                    self.entries[self.selectedCell[0]][self.selectedCell[1]].remove(int(event.char))

        if event.char == ' ':
            if self.currentMode == 'LARGE':
                self.currentMode = 'SMALL'
            else:
                self.currentMode = 'LARGE'

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
        for x in range(0, 3):
            for y in range(0, 3):
                miniGrid = tk.Frame(master=master)
                miniGrid.grid(row=x, column=y)

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
                # TODO: Pass the clicks up to the minigrid to be detected, currently broken
                labels[3 * x + y].bindtags((miniGrid,) + labels[3 * x + y].bindtags())

                labels[3 * x + y]['font'] = self.smallNumberFont
                labels[3 * x + y].grid(row=x, column=y)
        return miniGrid

    def update(self):
        # TODO: Unify both types of labels into one, then overwriting isnt a problem

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

                        if self.isInLargeMode[3 * x1 + x2][3 * y1 + y2]:
                            currentEntry = self.entries[3 * x1 + x2][3 * y1 + y2]

                            if self.selectedCell[0] == 3*x1 + x2 and self.selectedCell[1] == 3*y1 + y2:
                                if self.currentMode == 'LARGE':
                                    color = '#FFFF00'
                                else:
                                    color = '#FF00FF'
                            else:
                                color = '#FFFFFF'
                            self.labels[3 * x1 + x2][3 * y1 + y2] = self.buildLargeLabel(smallGrid, currentEntry, color)

                            self.labels[3 * x1 + x2][3 * y1 + y2].grid(row=x2, column=y2, padx=1, pady=1)

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
                            self.labels[3*x1 + x2][3*y1 + y2] = self.buildSmallLabel(smallGrid, self.entries[3*x1+x2][3*y1+y2], color)

                            clickDetector = self.onClick(3 * x1 + x2, 3 * y1 + y2)
                            self.labels[3 * x1 + x2][3 * y1 + y2].bind('<Button-1>', clickDetector)

if __name__ == '__main__':
    window = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)

    sudoku = SudokuGrid(window)
    window.mainloop()
