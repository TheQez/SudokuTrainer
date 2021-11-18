import tkinter as tk
from typing import List


class TacticVisualiserUI:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.tactics = []
        self.tabs = []
        self.visualiser = tk.Canvas(master=self.window, width=220, height=524, bg='#FFFFFF', bd=0, highlightthickness=0, relief='ridge')
        self.visualiser.grid(row=0, column=0)
        self.activeTactic = None

        self.update()

    def buildTacticTab(self, window, text, index, active):
        tabFrame = tk.Frame(master=window, width=200, height=50)
        if active:
            bgcolor = '#FF0000'
        else:
            bgcolor = '#DCDCDC'

        tab = tk.Canvas(master=tabFrame, width=200, height=50, bg=bgcolor, bd=0, highlightthickness=0, relief='ridge')
        tabName = tab.create_text((10, 25), text=text, anchor=tk.W, fill='#000000')
        tab.place(x=0, y=0)
        pixel = tk.PhotoImage(width=1, height=1)
        if not index == 0:
            upButtonCommand = lambda event: self.swapTabs(index, index-1)
            upButton = tk.Label(master=tab, image=pixel, height=10, width=10, anchor=tk.W, bg='#AAAAAA', bd=0)
            upButton.bind("<Button-1>", upButtonCommand)
            upButton.place(x=150, y=20)
        if not index == len(self.tactics)-1:
            downButtonCommand = lambda event: self.swapTabs(index, index + 1)
            downButton = tk.Label(master=tab, image=pixel, height=10, width=10, anchor=tk.W, bg='#AAAAAA', bd=0)
            downButton.bind("<Button-1>", downButtonCommand)
            downButton.place(x=180, y=20)
        return tabFrame

    def swapTabs(self, index1, index2):
        self.tactics[index1], self.tactics[index2] = self.tactics[index2], self.tactics[index1]
        self.update()

    def update(self):
        #Go through each tab and place them
        y = 10
        self.tabs = []
        for i in range(0, len(self.tactics)):
            tactic = self.tactics[i]
            if tactic == self.activeTactic:
                isActive = True
            else:
                isActive = False
            self.tabs.append(self.buildTacticTab(self.window, tactic.__class__.__name__, i, isActive))
            self.tabs[i].place(x=10, y=y)
            y += 60

