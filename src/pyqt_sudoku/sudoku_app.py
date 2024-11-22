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
        self.main_window.key_esc_pressed.connect(self.quit)


def launch_app():
    """Function to launch the app."""
    app = SudokuApp()
    app.main_window.show()
    app.exec()
