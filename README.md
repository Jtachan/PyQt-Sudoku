# PyQt-Sudoku

This repo is a small project to display a Sudoku board created only with PyQt6 elements.

## 🐍 Python Setup

**Requirements**

- Python 3.8 or higher

**Installation**

There is two possible installations:

1. _Install via pip_ (recommended)

For this method make use of 'pip' and 'git':

````bash
pip install git+https://github.com/Jtachan/PyQt-Sudoku.git
````

2. _Install locally_

First, clone the repo at your desired location:
````commandline
git clone https://github.com/Jtachan/PyQt-Sudoku.git
````

Then, prepare your environment and install locally:
```
pip install .
```

## 🏃 Usage

Once the repo is installed, run the following command at the terminal:

```bash
QSudokuApp
```

### Buttons

1. **New game**

To start, click the 'New game' button.
A new sudoku puzzle is then created based on the chosen difficulty.
There are three difficulty settings: _Easy_, _Medium_ and _Hard_. 

> Note: All generated puzzles have one single solution.

2. **Hints**

The 'Hint' button will give you some help when required.
You can expect two possible outcome when the button is pressed:

- A random cell will be filled with the correct number, represented in green.
- One of your numbers is colored red, only if it is incorrect.

3. **Check numbers**

When the 'check numbers' is pressed, all written numbers are compared against the solution.
Each incorrect number is printed red, and each correct number is printed green.

### **Exit the game**

To close the game, press the key 'ESC' or clock on the 'X' at the top right of the window.
