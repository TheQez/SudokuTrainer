from SudokuGrid import SudokuGrid as SudokuGrid
import copy
import random
from tactics.HiddenSingle import HiddenSingle
from tactics.NakedDouble import NakedDouble

def generateSudoku() -> SudokuGrid:
    while True:
        sudoku = SudokuGrid()
        sudoku = sudoku.bruteForce(solutionsCutoff=1, randomised=True)[0]
        while True:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            if sudoku.entries[x][y] not in range(1, 10):
                continue
            sudoku.entries[x][y] = None
            if not len(sudoku.solutions(solutionsCutoff=2)) == 1:
                print('Not valid, trying again')
                break
            tactics = getRequiredTactics(sudoku)[1]
            if tactics == None:
                print('Too hard, trying again')
                break
            if NakedDouble in tactics:
                return sudoku

def getRequiredTactics(sudoku: SudokuGrid):
    tactics = set()
    sudoku = copy.deepcopy(sudoku)
    while True:
        if sudoku.isSolved():
            return sudoku, tactics
        newSudoku, _, _, tactic = sudoku.getTactic()
        if tactic == None:
            return None, None
        if tactic not in tactics:
            tactics.add(tactic)
        sudoku = newSudoku