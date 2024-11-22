"""Module containing only the main window for the application."""

from __future__ import annotations

import os.path
import random
from typing import ClassVar, Iterator, Optional

from PyQt6 import QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt, pyqtSignal
from sudoku import Sudoku

# RGB Colors
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 250)


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

    key_esc_pressed = pyqtSignal()

    def __init__(self) -> None:
        """Constructor of SudokuMainWindow."""
        super().__init__()
        uic.loadUi(SudokuMainWindow.UI_FILE_PATH, self)

        new_game_button = self.findChild(QtWidgets.QPushButton, "newGameButton")
        hint_button = self.findChild(QtWidgets.QPushButton, "hintButton")

        new_game_button.clicked.connect(self.create_new_game)
        hint_button.clicked.connect(self.provide_a_hint)

        self._difficulty_combobox: QtWidgets.QComboBox = self.findChild(
            QtWidgets.QComboBox, "difficultyComboBox"
        )

        self.board = []
        self.solved_board = []
        self._reset_board()

    def get_cell(self, row_idx: int, col_idx: int) -> QtWidgets.QTextEdit:
        """Obtaining a single cell."""
        return self.findChild(QtWidgets.QTextEdit, f"cell_{row_idx}_{col_idx}")

    def create_new_game(self) -> None:
        """Creates a new sudoku game.

        When a new game is created:
            - All the cells are cleared and set to read and write.
            - A new sudoku puzzle (with only one solution) is created and the
              solution is stored.
            - The initial values are defined at each cell. These cells are set to
              read only.
        """
        self._reset_board()

        if self._difficulty_combobox.currentText() == "Easy":
            difficulty_level = 0.3
        elif self._difficulty_combobox.currentText() == "Medium":
            difficulty_level = 0.45
        else:
            difficulty_level = 0.6

        while True:
            puzzle = Sudoku(seed=random.randint(0, 500)).difficulty(difficulty_level)
            if puzzle.has_multiple_solutions():
                continue
            self.board = puzzle.board
            self.solved_board = puzzle.solve().board
            break

        for row_idx, row_values in enumerate(self.board):
            for col_idx, cell_value in enumerate(row_values):
                if cell_value is None:
                    continue
                self._set_cell_value(
                    cell=self.get_cell(row_idx, col_idx),
                    value=cell_value,
                    read_only=True,
                    rgb_color=BLACK,
                )

        self.findChild(QtWidgets.QPushButton, "hintButton").setEnabled(True)

    def provide_a_hint(self) -> None:
        """Updates one cell of the current board to provide a hint to the user."""
        row_indexes, col_indexes = list(range(9)), list(range(9))
        random.shuffle(row_indexes)
        random.shuffle(col_indexes)

        for row_idx in row_indexes:
            for col_idx in col_indexes:
                board_value = self.board[row_idx][col_idx]
                correct_value = self.solved_board[row_idx][col_idx]

                if board_value == correct_value:
                    continue

                if board_value is None:
                    # Cell is empty.
                    new_cell_value = correct_value
                    color = GREEN
                else:
                    # Cell has incorrect value.
                    new_cell_value = board_value
                    color = RED

                self._set_cell_value(
                    cell=self.get_cell(row_idx, col_idx),
                    value=new_cell_value,
                    rgb_color=color,
                )
                return

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
        rgb_color: tuple[int, int, int] = BLUE,
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
        cell.setFontPointSize(15)

        # Obtain cell coordinates & updating the stored values.
        if value is not None:
            *_, row_idx, col_idx = cell.objectName().split("_")
            self.board[int(row_idx)][int(col_idx)] = int(value)

        cell.textChanged.connect(lambda: self._validate_cell_text(cell))

    def _iterate_over_all_cells(self) -> Iterator[QtWidgets.QTextEdit]:
        """Iteration over all the cells at the board."""
        for row_idx in range(9):
            for col_idx in range(9):
                yield self.get_cell(row_idx, col_idx)

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

    def keyPressEvent(self, event: Optional[QtGui.QKeyEvent]):
        """Introcing the functionality to close the app when ESC is pressed."""
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_Escape:
            self.key_esc_pressed.emit()
