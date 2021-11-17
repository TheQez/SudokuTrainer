import tkinter as tk
from typing import List


class TacticVisualiserUI:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.tactics = []
        self.visualiser = tk.Canvas(master=self.window, width=220, height=524, bg='#FFFFFF', bd=0, highlightthickness=0, relief='ridge')
        self.visualiser.grid(row=0, column=0)
        self.activeTactic = None

        self.update()

    def update(self):
        #Go through each tab and place them
        y = 10
        for tactic in self.tactics:
            if tactic == self.activeTactic:
                isActive = True
            else:
                isActive = False
            tab = buildTacticTab(self.window, tactic.__name__, isActive)
            tab.place(x=10, y=y)
            y += 60


def buildTacticTab(window, text, active):
    tabFrame = tk.Frame(master=window, width=200, height=50)
    if active:
        bgcolor = '#FF0000'
    else:
        bgcolor = '#DCDCDC'
    tab = tk.Canvas(master=tabFrame, width=200, height=50, bg=bgcolor, bd=0, highlightthickness=0, relief='ridge')
    tabName = tab.create_text((10, 25), text=text, anchor=tk.W, fill='#000000')
    tab.place(x=0, y=0)
    return tabFrame
