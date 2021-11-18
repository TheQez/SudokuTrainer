from SudokuGrid import SudokuGrid as SudokuGrid
import copy
import random
from tactics.HiddenSingle import HiddenSingle
from tactics.NakedDouble import NakedDouble


def generateSudoku(tactics) -> SudokuGrid:
    while True:
        sudoku = SudokuGrid()
        sudoku = sudoku.bruteForce(solutionsCutoff=1, randomised=True)[0]
        sudoku.tactics = tactics
        while True:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            if sudoku.entries[x][y] not in range(1, 10):
                continue
            sudoku.entries[x][y] = None
            if not len(sudoku.solutions(solutionsCutoff=2)) == 1:
                print('Not valid, trying again')
                break
            usedTactics = getRequiredTactics(sudoku)[1]
            if usedTactics is None:
                print('Too hard, trying again')
                break
            if tactics[-1].__class__ in [tactic.__class__ for tactic in usedTactics]:
                return sudoku


def getRequiredTactics(sudoku: SudokuGrid):
    tactics = set()
    sudoku = copy.deepcopy(sudoku)
    while True:
        if sudoku.isSolved():
            return sudoku, tactics
        newSudoku, _, _, _, tactic = sudoku.getTactic()
        if tactic is None:
            return None, None
        if tactic not in tactics:
            tactics.add(tactic)
        sudoku = newSudoku
