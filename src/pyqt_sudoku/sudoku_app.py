"""Here is contained the main QApplication to launch the game."""

import sys

from PyQt6.QtWidgets import QApplication 

from pyqt_sudoku.sudoku_main_win import SudokuMainWindow


class SudokuApp(QApplication):
    """Main QApp to control the sudoku game."""

    def __init__(self):
        """Constructor of the class.
        It prepares the sudoku window automatically.
        """
        super().__init__(sys.argv)
        self.main_window = SudokuMainWindow()

    def exec(*args, **kwargs):
        """Overrides the original method to also display the window."""
        self.main_window.show()
        super().exec(*args, **kwargs)


def launch_app():
    """Function to launch the app."""
    app = SudokuApp()
    app.exec()