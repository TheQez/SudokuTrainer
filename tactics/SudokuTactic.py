from __future__ import annotations
from abc import ABC, abstractmethod
import SudokuGrid
from typing import List, Set


class SudokuTactic(ABC):
    applyType = tuple[SudokuGrid, List[List[Set]], List[List[Set]]]

    @abstractmethod
    def apply(self, sudoku: SudokuGrid) -> applyType:
        pass

    @staticmethod
    def isInRow(sudoku: SudokuGrid.SudokuGrid, number: int, row: int) -> bool:
        for i in range(0, 9):
            if sudoku.isInLargeMode[row][i]:
                if sudoku.entries[row][i] == number:
                    return True
        return False

    @staticmethod
    def isInColumn(sudoku: SudokuGrid.SudokuGrid, number: int, column: int) -> bool:
        for i in range(0, 9):
            if sudoku.isInLargeMode[i][column]:
                if sudoku.entries[i][column] == number:
                    return True
        return False

    # Checks if number appears in same box as (x, y)
    @staticmethod
    def isInBox(sudoku: SudokuGrid.SudokuGrid, number: int, x: int, y: int) -> bool:
        for i in range(0, 3):
            for j in range(0, 3):
                if sudoku.isInLargeMode[x-(x % 3)+i][y-(y % 3)+j]:
                    if sudoku.entries[x-(x % 3)+i][y-(y % 3)+j] == number:
                        return True
        return False

    # Checks the number of pencil markings in a row
    @staticmethod
    def numInRow(sudoku: SudokuGrid.SudokuGrid, number: int, row: int) -> int:
        count = 0
        for i in range(0, 9):
            if not sudoku.isInLargeMode[row][i] and number in sudoku.entries[row][i]:
                count += 1
        return count

    @staticmethod
    def numInColumn(sudoku: SudokuGrid.SudokuGrid, number: int, column: int) -> int:
        count = 0
        for i in range(0, 9):
            if not sudoku.isInLargeMode[i][column] and number in sudoku.entries[i][column]:
                count += 1
        return count

    @staticmethod
    def numInBox(sudoku: SudokuGrid.SudokuGrid, number: int, x: int, y: int) -> int:
        count = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if not sudoku.isInLargeMode[x-(x % 3)+i][y-(y % 3)+j]:
                    if number in sudoku.entries[x-(x % 3)+i][y-(y % 3)+j]:
                        count += 1
        return count

    @staticmethod
    def isConnected(x1: int, y1: int, x2: int, y2: int) -> bool:
        if x1 == x2 or y1 == y2:
            return True

        # If in the same box
        if (x1 // 3 == x2 // 3) and (y1 // 3 == y2 // 3):
            return True

        return False
