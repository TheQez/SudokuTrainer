import tkinter as tk
from typing import List


class TacticVisualiserUI:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.activeTactics = []
        self.inactiveTactics = []
        self.activeTabs = []
        self.activeTacticBoard = tk.Canvas(master=self.window, width=220, height=524, bg='#FFFFFF', bd=0, )
        self.activeTacticBoard.grid(row=0, column=0)
        self.inactiveTacticBoard = tk.Canvas(master=self.window, width=220, height=524, bg='#FFFFFF', bd=0)
        self.inactiveTacticBoard.grid(row=0, column=1)
        self.highlightedTactic = None

        self.update()

    def buildTacticTab(self, window, text, index, highlighted, active):
        tabFrame = tk.Frame(master=window, width=200, height=50)
        if highlighted:
            bgcolor = '#FF0000'
        else:
            bgcolor = '#DCDCDC'

        tab = tk.Canvas(master=tabFrame, width=200, height=50, bg=bgcolor, bd=0, highlightthickness=0, relief='ridge')
        tabName = tab.create_text((10, 25), text=text, anchor=tk.W, fill='#000000')
        tab.place(x=0, y=0)
        pixel = tk.PhotoImage(width=1, height=1)

        if active:
            numTactics = len(self.activeTactics)
        else:
            numTactics = len(self.inactiveTactics)
        if not index == 0:
            upButtonCommand = lambda event: self.shiftTabs(index, index - 1, active)
            upButton = tk.Label(master=tab, image=pixel, height=10, width=10, anchor=tk.W, bg='#AAAAAA', bd=0)
            upButton.bind("<Button-1>", upButtonCommand)
            upButton.place(x=130, y=20)
        if not index == numTactics - 1:
            downButtonCommand = lambda event: self.shiftTabs(index, index + 1, active)
            downButton = tk.Label(master=tab, image=pixel, height=10, width=10, anchor=tk.W, bg='#AAAAAA', bd=0)
            downButton.bind("<Button-1>", downButtonCommand)
            downButton.place(x=150, y=20)
        acrossButtonCommand = lambda event: self.swapTab(index, active)
        acrossButton = tk.Label(master=tab, image=pixel, height=10, width=10, anchor=tk.W, bg='#AAAAAA', bd=0)
        acrossButton.bind("<Button-1>", acrossButtonCommand)
        acrossButton.place(x=170, y=20)
        return tabFrame

    def shiftTabs(self, index1, index2, isActive):
        if isActive:
            self.activeTactics[index1], self.activeTactics[index2] = self.activeTactics[index2], self.activeTactics[index1]
        else:
            self.inactiveTactics[index1], self.inactiveTactics[index2] = self.inactiveTactics[index2], self.inactiveTactics[index1]
        self.update()

    def swapTab(self, index, isActive):
        if isActive:
            self.inactiveTactics.append(self.activeTactics[index])
            self.activeTactics.pop(index)
        else:
            self.activeTactics.append(self.inactiveTactics[index])
            self.inactiveTactics.pop(index)
        self.update()

    def update(self):
        for child in self.activeTacticBoard.winfo_children():
            child.destroy()
        for child in self.inactiveTacticBoard.winfo_children():
            child.destroy()

        y = 10
        self.activeTabs = []
        for i in range(0, len(self.activeTactics)):
            tactic = self.activeTactics[i]
            if tactic == self.highlightedTactic:
                isHighlighted = True
            else:
                isHighlighted = False
            self.activeTabs.append(self.buildTacticTab(self.activeTacticBoard, tactic.__class__.__name__, i, isHighlighted, True))
            self.activeTabs[i].place(x=10, y=y)
            y += 60

        y = 10
        self.inactiveTabs = []
        for i in range(0, len(self.inactiveTactics)):
            tactic = self.inactiveTactics[i]
            if tactic == self.highlightedTactic:
                isHighlighted = True
            else:
                isHighlighted = False
            self.inactiveTabs.append(self.buildTacticTab(self.inactiveTacticBoard, tactic.__class__.__name__, i, isHighlighted, False))
            self.inactiveTabs[i].place(x=10, y=y)
            y += 60


