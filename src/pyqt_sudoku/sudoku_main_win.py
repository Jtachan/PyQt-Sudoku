"""Module containing only the main window for the application."""
import os.path
from PyQt6 import QtWidgets, uic
from sudoku import Sudoku


class SudokuMainWindow(QtWidgets.QMainWindow):
    """Class holding the main window of the application."""

    UI_FILE_PATH = os.path.abspath(__file__).replace(".py", ".ui")

    def __init__(self):
        """Constructor of SudokuMainWindow.
        It automatically calls the 'show()' method.
        """
        super().__init__()
        uic.loadUi(SudokuMainWindow.UI_FILE_PATH, self)

        self.new_game_button: QtWidgets.QPushButton = self.findChild(
            QtWidgets.QPushButton, "newGameButton"
        )
        self.new_game_button.clicked.connect(self.create_new_game)

        self.board = []
        self._reset_board()

        self.show()

    def create_new_game(self):
        """Creates a new sudoku game."""
        self._reset_board()

        puzzle = Sudoku().difficulty(0.3)
        self.board = puzzle.board
        print(puzzle)

        for row_idx, row_values in enumerate(self.board):
            for col_idx, cell_value in enumerate(row_values):

                if cell_value is None:
                    continue

                cell = self.findChild(
                    QtWidgets.QTextEdit, f"cell_{row_idx}_{col_idx}"
                )
                cell.setText(str(cell_value))
                cell.setReadOnly(True)

    def _reset_board(self):
        self.board = [[None] * 9 for _ in range(9)]

        for row_idx in range(9):
            for col_idx in range(9):
                cell: QtWidgets.QTextEdit = self.findChild(
                    QtWidgets.QTextEdit, f"cell_{row_idx}_{col_idx}"
                )
                cell.clear()
                cell.setReadOnly(False)
