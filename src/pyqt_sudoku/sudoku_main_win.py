"""Module containing only the main window for the application."""
import os.path
from PyQt6 import QtWidgets, uic


class SudokuMainWindow(QtWidgets.QMainWindow):
    """Class holding the main window of the application."""

    UI_FILE_PATH = os.path.abspath(__file__).replace(".py", ".ui")

    def __init__(self):
        """Constructor of SudokuMainWindow.
        It automatically calls the 'show()' method.
        """
        super().__init__()
        uic.loadUi(SudokuMainWindow.UI_FILE_PATH, self)
        self.show()
