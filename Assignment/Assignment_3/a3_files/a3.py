"""
CSSE1001 Assignment 3
Semester 1, 2017
"""

import tkinter as tk
from tkinter import messagebox

import model
import view
from game_regular import RegularGame

__author__ = "Jiabo Qin"
__email__ = "qinjiabo1990@gmail.com"

__version__ = "1.0.0"


# Once you have created your basic gui (LoloApp), you can delete this class
# and replace it with the following:
# from base import BaseLoloApp
from base import BaseLoloApp
# Define your classes here
"""Task1"""
class LoloApp(BaseLoloApp):
    def __init__(self, ):

class StatusBar(tk.Frame):
    """{game_mode_name} Game (Left)
    The name of whichever game mode the player is currently playing.
        Score: {score} (Right)
    Must be updated whenever the player's score changes.
    """
    def __inut__(self):
        pass
    def set_game(game_mode):
        pass
    def set_score(score):
        pass

class LoloLogo(tk.Canvas):
    """draw a simple logo"""
    def __init__(self, master):
        super().__init__(master)
        master.title("LoLo")

        self._canvas = tk.Canvas(master, bg="white", width=600, height=700)
        self._canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._canvas.create_rectangle(120,20,140,90, fill= "#6d4876", outline="#6d4876")
        self._canvas.create_rectangle(120,90,180,110, fill= "#6d4876", outline="#6d4876")
        self._canvas.create_oval(210, 40, 270, 100, outline="#6d4876", width=20)
        self._canvas.create_rectangle(310,20,330,90, fill= "#6d4876", outline="#6d4876")
        self._canvas.create_rectangle(310,90,370,110, fill= "#6d4876", outline="#6d4876")
        self._canvas.create_oval(400, 40, 460, 100, outline="#6d4876", width=20)

"""
4.4 File Menu
New game: Restarts the game
Exit: Exits the application

4.5 lightning button
Implement a button, which when pressed,
deletes a random tile from the game grid.

4.6 Dialog
1). Invalid Activation: If the user attempts to activate a tile that
cannot be activated, show an error dialog with an appropriate message.
2). Game Over: The the game ends, show a dialog informing the user of
their score.

4.7 Keyboard Shortcuts
Implement the following keyboard shortcuts:

ctrl + n: Start new game.
ctrl + l: Performs the lightning action.
#for mac is CMD(command).
"""

"""Task2"""
class AutoPlayingGame(BaseLoloApp):
"""will record in the high score, so need to entry name"""
    def __init__(master)

"""
5.2 Loading Screen
Logo:
Buttons:
Name Entry:
Auto Playing Game:

5.3 High Score Window
open a new window through a button. like example
a.best player
b.text leaderboard
c.logo: reuse from task1
d.Buttons:play game, exit game, high scores, open-ended
e.name entry
f.auto playing game
"""

"""Task3"""
"""
6.1
a.loading screen, add Game Mode under New Game. open new window to choose mode
b.dialog box if not enter name

"""


def main():
    pass
    # Your GUI instantiation code here

root = tk.Tk()
app = LoloLogo(root)
root.mainloop()

if __name__ == "__main__":
    main()






















