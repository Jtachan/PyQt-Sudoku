"""Module containing only the main window for the application."""

from __future__ import annotations

import os.path
import random
from typing import ClassVar, Iterator, Optional

from PyQt6 import QtGui, QtWidgets, uic, QtCore
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

    key_esc_pressed = QtCore.pyqtSignal()

    def __init__(self) -> None:
        """Constructor of SudokuMainWindow."""
        super().__init__()
        uic.loadUi(SudokuMainWindow.UI_FILE_PATH, self)

        new_game_button = self.findChild(QtWidgets.QPushButton, "newGameButton")
        self.hint_button = self.findChild(QtWidgets.QPushButton, "hintButton")
        self.check_numbers_button = self.findChild(
            QtWidgets.QPushButton, "checkNumbersButton"
        )
        self.difficulty_combobox: QtWidgets.QComboBox = self.findChild(
            QtWidgets.QComboBox, "difficultyComboBox"
        )

        new_game_button.clicked.connect(self.create_new_game)
        self.hint_button.clicked.connect(self.provide_a_hint)
        self.check_numbers_button.clicked.connect(self.check_numbers_in_cells)

        self.timer = QtCore.QTimer(parent=self)
        self.timer.timeout.connect(self.update_displayed_time)
        self.seconds_on_game = 0

        self.board = []
        self.solved_board = []
        self._reset_board()

    def get_cell(self, row_idx: int, col_idx: int) -> QtWidgets.QTextEdit:
        """Obtaining a single cell."""
        return self.findChild(QtWidgets.QTextEdit, f"cell_{row_idx}_{col_idx}")

    def enable_hint_buttons(self, enabled: bool):
        """Enabling/Disabling the buttons that provide hints to the user."""
        for button_name in ("hintButton", "checkNumbersButton"):
            self.findChild(QtWidgets.QPushButton, button_name).setEnabled(enabled)

    def iterate_over_all_cells(self) -> Iterator[QtWidgets.QTextEdit]:
        """Iteration over all the cells at the board."""
        for row_idx in range(9):
            for col_idx in range(9):
                yield self.get_cell(row_idx, col_idx)

    @property
    def is_board_solved(self) -> bool:
        """If the sudoku puzzle is solved"""
        return self.board == self.solved_board

    def update_displayed_time(self) -> None:
        """Updating the time displayed at the status bar. The time is
        updated by 1 second.
        """
        self.seconds_on_game += 1
        minutes, seconds = divmod(self.seconds_on_game, 60)
        hours, minutes = divmod(minutes, 60)
        self.statusBar().showMessage(f"{hours:02}:{minutes:02}:{seconds:02}")

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

        if self.difficulty_combobox.currentText() == "Easy":
            difficulty_level = 0.3
        elif self.difficulty_combobox.currentText() == "Medium":
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
                cell = self.get_cell(row_idx, col_idx)
                cell.setEnabled(True)
                if cell_value is None:
                    continue
                self._set_cell_value(
                    cell=self.get_cell(row_idx, col_idx),
                    value=cell_value,
                    read_only=True,
                    rgb_color=BLACK,
                )

        self.enable_hint_buttons(True)
        self.timer.start(1000)
        self.seconds_on_game = 0
        self.statusBar().showMessage("00:00:00")

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

    def check_numbers_in_cells(self):
        """Iterates over all the cells to paint"""
        for cell in self.iterate_over_all_cells():
            if cell.isReadOnly():
                # Ignoring the cells that were set as the initial state.
                continue

            if cell.toPlainText() == "":
                continue

            cell_row, cell_col = [int(idx) for idx in cell.objectName().split("_")[-2:]]
            board_number = self.board[cell_row][cell_col]
            correct_number = self.solved_board[cell_row][cell_col]

            self._set_cell_value(
                cell=cell,
                value=board_number,
                rgb_color=RED if board_number != correct_number else GREEN,
            )

    def _reset_board(self) -> None:
        """Resetting/Clearing the board.

        The following steps are performed:
            1. All values within the board are set to 'None'.
            2. Every cell (QTextEdit) is cleared to an initial status.
        """
        self.board = [[None] * 9 for _ in range(9)]
        for cell in self.iterate_over_all_cells():
            self._set_cell_value(cell=cell, value=None)
            cell.setEnabled(False)

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
        cell.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        cell.setFontPointSize(15)

        # Obtain cell coordinates & updating the stored values.
        if value is not None:
            *_, row_idx, col_idx = cell.objectName().split("_")
            self.board[int(row_idx)][int(col_idx)] = int(value)

        cell.textChanged.connect(lambda: self._validate_cell_text(cell))

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
        
    # ***********************
    # Qt overloaded functions
    # ***********************

    # ruff: noqa: N802
    def keyPressEvent(self, event: Optional[QtGui.QKeyEvent]) -> None:
        """Introduced the functionality to close the app when ESC is pressed."""
        super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.key_esc_pressed.emit()
