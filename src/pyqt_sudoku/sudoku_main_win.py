"""Module containing only the main window for the application."""

from __future__ import annotations

import os.path
import random
from typing import ClassVar, Iterator, Optional

from PyQt6 import QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
from sudoku import Sudoku

# RGB Colors
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (255, 0, 0)


class SudokuMainWindow(QtWidgets.QMainWindow):
    """Class holding the main window of the application."""

    UI_FILE_PATH = os.path.abspath(__file__).replace(".py", ".ui")
    _VALID_CELL_VALUES: ClassVar[set[str]] = {
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    }

    def __init__(self) -> None:
        """Constructor of SudokuMainWindow."""
        super().__init__()
        uic.loadUi(SudokuMainWindow.UI_FILE_PATH, self)

        self.new_game_button: QtWidgets.QPushButton = self.findChild(
            QtWidgets.QPushButton, "newGameButton"
        )
        self.new_game_button.clicked.connect(self.create_new_game)

        self.board = []
        self._reset_board()

    def create_new_game(self) -> None:
        """Creates a new sudoku game."""
        self._reset_board()

        puzzle = Sudoku(seed=random.randint(0, 500)).difficulty(0.3)
        self.board = puzzle.board

        for row_idx, row_values in enumerate(self.board):
            for col_idx, cell_value in enumerate(row_values):
                if cell_value is None:
                    continue
                cell = self.findChild(QtWidgets.QTextEdit, f"cell_{row_idx}_{col_idx}")
                self._set_cell_value(
                    cell=cell, value=cell_value, read_only=True, rgb_color=GREEN
                )

    def _reset_board(self) -> None:
        """Resetting/Clearing the board.

        The following steps are performed:
            1. All values within the board are set to 'None'.
            2. Every cell (QTextEdit) is cleared to an initial status.
        """
        self.board = [[None] * 9 for _ in range(9)]
        for cell in self._iterate_over_all_cells():
            self._set_cell_value(cell=cell, value=None)

    def _set_cell_value(
        self,
        cell: QtWidgets.QTextEdit,
        value: Optional[int | str],
        read_only: bool = False,
        rgb_color: tuple[int, int, int] = BLACK,
    ) -> None:
        """Sets the value of a single cell.

        Parameters
        ----------
        cell : QTextEdit
            Widget corresponding to the cell.
        value : int, optional
            Value to set within the cell. If 'None' is passed, the cell is cleared.
        read_only : bool
            Boolean to define if the widget should be read only.
        """
        try:
            cell.disconnect()
        except TypeError:
            # No signals connected
            pass

        cell.setTextColor(QtGui.QColor.fromRgb(*rgb_color))
        if value is None:
            cell.clear()
        else:
            cell.setText(str(value))
        cell.setReadOnly(read_only)
        cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cell.textChanged.connect(lambda: self._validate_cell_text(cell))

    def _iterate_over_all_cells(self) -> Iterator[QtWidgets.QTextEdit]:
        """Iteration over all the cells at the board."""
        for row_idx in range(9):
            for col_idx in range(9):
                cell: QtWidgets.QTextEdit = self.findChild(
                    QtWidgets.QTextEdit, f"cell_{row_idx}_{col_idx}"
                )
                yield cell

    def _validate_cell_text(self, cell: QtWidgets.QTextEdit) -> None:
        """Validation of the text contained within a cell.

        Within the sudoku board, only the numbers from 1 to 9 are allowed.
        The validation of a cell consist in:
            1. If the length is longer than 1 character, only the first character
               remains.
            2. If the character is not a number or an invalid number, the cell
               is cleared.

        The validation is performed only for those cells that are modifiable by the
        user.
        """
        if cell.isReadOnly():
            return
        text = cell.toPlainText()
        if len(text) > 1:
            text = text[0]
        if text not in self._VALID_CELL_VALUES:
            text = None
        self._set_cell_value(cell=cell, value=text)
