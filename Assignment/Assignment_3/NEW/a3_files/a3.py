"""
CSSE1001 Assignment 3
Semester 1, 2017
"""

__author__ = "Jiabo Qin"
__email__ = "qinjiabo1990@gmail.com"

__version__ = "1.1.2"

import tkinter as tk
from tkinter import messagebox
from game_regular import RegularGame
from highscores import HighScoreManager
from game_lucky7 import Lucky7Game
from game_make13 import Make13Game
from game_regular import RegularGame
from game_unlimited import UnlimitedGame
from base import BaseLoloApp
import model
import view
import random


class LoloApp(BaseLoloApp):
    """Main class for running Lolo game"""
    
    def __init__(self, master, game=None, grid_view=None):
        """Constructor

        Parameters:
            master (tk.Tk|tk.Frame): The parent widget.
            game (model.AbstractGame): The game to play. Defaults to a
                                       game_regular.RegularGame.
            grid_view (view.GridView): The view to use for the game. Optional.

        Raises:
            ValueError: If grid_view is supplied, but game is not.
        """
        super().__init__(master, game, grid_view)
        self._grid_view.pack_forget()
        self._master.title("Lolo " + self._game.get_name() + " Game")
        self._master.geometry("800x900")
        self.menu()
        self.create_logo_frame()
        self.canvas = LoloLogo(self.logo_frame)
        self.status_bar = StatusBar(self.logo_frame, self._game)
        self._grid_view.configure()
        self._grid_view.pack(side=tk.TOP, expand=False)
        self.lightning_button()

    def menu(self):
        """a menu contains new game, high scores and exit"""
        self.menubar = tk.Menu(self._master)
        self._master.config(menu=self.menubar)
        self.filemenu = tk.Menu(self.menubar)        
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New Game", command = self.reset)
        self.filemenu.add_command(label="High Score", command = self.highscore)
        self.filemenu.add_command(label="Exit", command = self.exit)
        self._master.bind("<Control-n>", self.reset)

    def exit(self) :
        """Close the application."""
        self._master.destroy()

    def reset(self, ev=None):
        """reset the game every parameters"""
        self._game.reset()
        self._game.set_score(0)
        self._grid_view.draw(self._game.grid, self._game.find_connections())
        self.lightning_num = 1
        self.lightning_button.configure(text="Lightning ("+ str(self.lightning_num) +")",
                                        fg ="black")
    def highscore(self):
        app.pack_forget()
        game = Scores(root)
        
    def create_logo_frame(self):
        """create a frame to put Logo in"""
        self.logo_frame = tk.Frame(self._master, width=600)
        self.logo_frame.pack(side=tk.TOP)

    def game_over(self):
        """finish the game"""
        self._game.game_over()
        return messagebox.showerror("Game Over", "Game Over, Your score is: {}".format(self._game.get_score()))

    def set_game(self):
        """return game modes"""
        self._mode_label.configure(text=self._game.get_name()+" Game")
        
    def set_score(self, points):
        """return the score of the game

        Parameters"
            points: set the initial value
        """
        self.status_bar._score_label.configure(text="Score: {}".format(self._game.get_score()))

    def bind_events(self):
        """Binds relevant events."""
        super().bind_events()
        self._game.on("score", self.set_score)

    def activate(self, position): 
        """Attempts to activate the tile at the given position.

        Parameters:
            position (tuple<int, int>): Row-column position of the tile.

        Raises:
            IndexError: If position cannot be activated.
        """
        if position is None:
            return

        if self._game.is_resolving():
            return

        if position in self._game.grid:

            if not self._game.can_activate(position):
                return messagebox.showerror("Invalid position", "Cannot activate this position")
            else :
                self.lightning_add()

            def finish_move():
                self._grid_view.draw(self._game.grid,
                                     self._game.find_connections())

            def draw_grid():
                self._grid_view.draw(self._game.grid)

            animation = self.create_animation(self._game.activate(position),
                                              func=draw_grid,
                                              callback=finish_move)
            animation()

    def remove(self, *positions):
        """Attempts to remove the tiles at the given positions.

        Parameters:
            *positions (tuple<int, int>): Row-column position of the tile.

        Raises:
            IndexError: If position cannot be activated.
        """
        if len(positions) is None:
            return

        if self._game.is_resolving():
            return

        def finish_move():
            self._grid_view.draw(self._game.grid,
                                 self._game.find_connections())
            self.lightning_finish()

        def draw_grid():
            self._grid_view.draw(self._game.grid)

        animation = self.create_animation(self._game.remove(*positions),
                                          func=draw_grid,
                                          callback=finish_move)
        animation()

    def lightning_button(self):
        """create a button for lightninig"""
        self.turns = 0
        self.lightning_num = 1
        self.lightning_button = tk.Button(self._master, text="Lightning (" +
                                          str(self.lightning_num) +")",
                                          command=self.lightning_excution)
        self.lightning_button.pack(side=tk.TOP, pady=10)
        self._master.bind("<Control-l>", self.lightning_excution)

    def lightning_add(self):
        """the lightning may add 1 every 20 turns"""
        self.turns += 1
        if self.turns == 20:
            self.turns = 0
            self.lightning_num += 1
            self.lightning_button.configure(text="Lightning ("+ str(self.lightning_num) +")",
                                            fg ="black")            

    def lightning_excution(self, ev=None):
        """run the lightning"""
        if self.lightning_num > 0:
            self.lightning_button.configure(text="choose a title", fg="red")
            self._grid_view.off('select', self.activate)
            self._grid_view.on('select', self.remove)
        else:
            messagebox.showerror("Sorry", "You have no chance")
        
    def lightning_finish(self):
        """the paramater of finishing to use lightning"""
        self.lightning_num -= 1
        self._grid_view.off('select', self.remove)
        self._grid_view.on('select', self.activate)
        self.lightning_button.configure(text="Lightning ("+ str(self.lightning_num) +")",
                                        fg ="black")

class StatusBar(tk.Frame):
    """the status bar dispaly the game modes and current scores"""
    
    def __init__(self, master, game):
        """Constructor

        Parameters:
            master (tk.Tk|tk.Frame): The parent widget.
            game (model.AbstractGame): The game to play. Defaults to a
                                       game_regular.RegularGame.

        """
        super().__init__(master)
        self._master = master
        self._game = game
        self.configure(width=500, height=50, bg=self._master.cget("bg"))
        self.pack(side=tk.TOP, fill=tk.BOTH)
        
        self._mode_label = tk.Label(self, text=self._game.get_name()+" Game",
                                    bg=self._master.cget("bg"))
        self._mode_label.pack(side=tk.LEFT, padx=10, pady=10)
        self._score_label = tk.Label(self, bg=self._master.cget("bg"),
                                     text="Score: 0")
        self._score_label.pack(side=tk.RIGHT, padx=10, pady=10)
    
        
class LoloLogo(tk.Canvas):
    """draw a LoLo logo"""
    
    def __init__(self, master):
        """Constructor

        Parameters:
            master: The parent widget.
        """
        super().__init__(master)
        self._master = master
        self.configure(width=600, height=120, bg=self._master.cget("bg"),
                       highlightthickness=0, relief='ridge')
        self.pack(side=tk.TOP)
        self.logo()

    def logo(self):
        """using rectangle and oval to draw Lolo"""
        self.create_rectangle(120,20,140,90, fill= "#6d4876", outline="#6d4876")
        self.create_rectangle(120,90,180,110, fill= "#6d4876", outline="#6d4876")
        self.create_oval(210, 40, 270, 100, outline="#6d4876", width=20)
        self.create_rectangle(310,20,330,90, fill= "#6d4876", outline="#6d4876")
        self.create_rectangle(310,90,370,110, fill= "#6d4876", outline="#6d4876")
        self.create_oval(400, 40, 460, 100, outline="#6d4876", width=20)


class AutoPlayingGame(BaseLoloApp):
    """Game will be played by itself"""
    
    def __init__(self, master, game=None, grid_view=None):
        """Constructor

        Parameters:
            master (tk.Tk|tk.Frame): The parent widget.
            game (model.AbstractGame): The game to play. Defaults to a
                                       game_regular.RegularGame.
            grid_view (view.GridView): The view to use for the game. Optional.

        Raises:
            ValueError: If grid_view is supplied, but game is not.
        """
        super().__init__(master, game, grid_view)
        self._grid_view.pack_forget()
        self._grid_view.configure()
        self._grid_view.pack(side=tk.TOP, expand=False)
        self._move_delay = 0
        self.move()
        
    def bind_events(self):
        """Binds relevant events."""
        self._game.on('resolve', self.resolve)

    def resolve(self, delay=None):
        """Makes a move after a given movement delay."""
        if delay is None:
            delay = self._move_delay

        self._master.after(delay, self.move)

    def move(self):
        """Finds a connected tile randomly and activates it."""
        connections = list(self._game.find_groups())

        if connections:
            cells = list()

            for connection in connections:
                for cell in connection:
                    cells.append(cell)

            self.activate(random.choice(cells))
        else:
            self.reset()

    def reset(self):
        """reset the game every parameters"""
        self._game.reset()
        self._grid_view.draw(self._game.grid, self._game.find_connections())
        self.move()


class LoadingScreen(tk.Frame):
    """create a interface that have many option"""
    
    def __init__(self, master):
        """Constructor

        Parameters:
            master: The parent widget.
        """
        super().__init__(master)
        self._master = master
        self._master.title("Lolo")
        self._master.geometry("900x800")
        self.configure()
        self.pack(side=tk.TOP)
        self.logo = LoloLogo(self)
        self.name_entry()
        self.autoplaying()
        self.optional_items()
        
    def name_entry(self):
        """create a widget to enter name and locate it"""
        self.entry_frame = tk.Frame(self)
        self.name = tk.Label(self.entry_frame, text="Your Name: ")
        self.name.pack(side=tk.LEFT)
        self.entry = tk.Entry(self.entry_frame, width=20)
        self.entry.pack(side=tk.LEFT)
        self.entry_frame.pack(side=tk.TOP, pady=10)

    def optional_items(self):
        """create four items to make choice and locate it"""
        self.items_frame = tk.Frame(self)
        self.play_game = tk.Button(self.items_frame, fg="blue", text="Play Game",
                                   command=self.play_game)
        self.play_game.pack(side=tk.TOP, pady=50, ipadx=150)
        self.play_game = tk.Button(self.items_frame, fg="blue", text="Game Modes",
                                   command=self.game_modes)
        self.play_game.pack(side=tk.TOP, pady=50, ipadx=150)        
        self.high_scores = tk.Button(self.items_frame, fg="blue", text="High Scores",
                                     command=self.scores)
        self.high_scores.pack(side=tk.TOP, pady=50, ipadx=150)
        self.high_scores = tk.Button(self.items_frame, fg="blue", text="Exit Game",
                                     command=self._master.destroy)
        self.high_scores.pack(side=tk.TOP, pady=50, ipadx=150)        
        self.items_frame.pack(side=tk.LEFT, padx=50, expand=True)
       
    def autoplaying(self):
        """call the function AutoPlayingGame and loacate it"""
        self.autoplay_frame = tk.Frame(self)
        self.running = AutoPlayingGame(self.autoplay_frame)
        self.autoplay_frame.pack(side=tk.RIGHT, expand=True)

    def play_game(self):
        """set the function of button paly game and loads it"""
        if len(self.entry.get()) == 0:
            messagebox.showerror("Attention", "Please entry your name!")
        else:
            app.pack_forget()
            game = LoloApp(root)

    def game_modes(self):
        """set the function of button game modes and loads it"""
        if len(self.entry.get()) == 0:
            messagebox.showerror("Attention", "Please entry your name!")
        else:
            app._master.wm_withdraw()
            self._pause = True
            self.gamemodes_window = GameModes(self._master)

    def scores(self):
        """set the function of button high scores and loads it"""
        app.pack_forget()
        game = Scores(root)

class Scores(tk.Frame):
    """create a new window to display high scores"""
    
    def __init__(self, master):
        """Constructor

        Parameters:
            master: The parent widget.
        """
        super().__init__(master)
        self._master = master
        self._master.title("High Scores :: {}.format(player[0])")
        self._master.geometry("600x600")
        self.configure()
        self.pack(side=tk.TOP)
        self.points()

    def points(self):
        """show the valuee of the highest details"""
        self.entry_frame = tk.Frame(self)
        self.name = tk.Label(self.entry_frame, text="Best Player:+player.items()[0] + with + player.values()[0] + points!")
        self.name.pack(side=tk.TOP)
        self.entry_frame.pack(side=tk.TOP, pady=10)

class GameModes(tk.Toplevel):
    """create a new window to display four modes of the game"""
    
    def __init__(self, master):
        """Constructor

        Parameters:
            master: The parent widget.
        """
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.configure()
        
        self.selections_frame = tk.Frame(self)
        self.selections_frame.pack(side=tk.LEFT, expand=True)

        self.options()

        self.autoplay_game(game=self.get_modes())

        self.buttons()

    def options(self):
        """set the option buttons"""
        self.v = tk.StringVar()
        self.v.set("regular")
        self.regular = tk.Radiobutton(self.selections_frame, fg="blue",
                                      variable=self.v, text="Regular Game",
                                      value="regular", command=self.set_autoplay)
        self.regular.pack(side=tk.TOP)
        self.regular = tk.Radiobutton(self.selections_frame, fg="blue",
                                      variable=self.v, text="Lucky 7 Game",
                                      value="lucky7", command=self.set_autoplay)
        self.regular.pack(side=tk.TOP)
        self.regular = tk.Radiobutton(self.selections_frame, fg="blue",
                                      variable=self.v, text="Make 13 Game",
                                      value="make13", command=self.set_autoplay)
        self.regular.pack(side=tk.TOP)
        self.regular = tk.Radiobutton(self.selections_frame, fg="blue",
                                      variable=self.v, text="Unlimited Game",
                                      value="unlimited", command=self.set_autoplay)
        self.regular.pack(side=tk.TOP)

    def autoplay_game(self, game):
        """call function AutoPlayingGame"""
        if game == None:
            game = RegularGame(types=3)
        self.autoplay_frame = tk.Frame(self)
        self.autoplay = AutoPlayingGame(self.autoplay_frame, game=game)
        self.autoplay_frame.pack(side=tk.TOP, expand=True)

    def buttons(self):
        """create to choice button"""
        self.button_frame = tk.Frame(self)
        self.play_game = tk.Button(self.button_frame, text="Play Game", command=self.start)
        self.play_game.pack(side=tk.LEFT, padx=5, pady=10)
        self.cancel = tk.Button(self.button_frame, text="Cancel", command=self.out)
        self.cancel.pack(side=tk.LEFT, padx=5, pady=10)
        self.button_frame.pack(side=tk.TOP)

    def get_modes(self):
        """provide four modes"""
        self.game_codes = {"regular": RegularGame(types=3),
                       "make13": Make13Game(goal_value=13),
                       "lucky7": Lucky7Game(lucky_value=7),
                       "unlimited": UnlimitedGame(types=4)}
        if self.v.get():
            return self.game_codes[self.v.get()]
        else:
            return RegularGame(types=3)

    def set_autoplay(self):
        """remove last autoplay and display current autoplay"""
        self.autoplay_frame.destroy()
        self.button_frame.pack_forget()
        self.autoplay_game(self.get_modes())
        self.button_frame.pack()

    def start(self):
        """set the function of button start game and loads it"""
        app.destroy()
        game = LoloApp(root, game=self.get_modes())
        game._master.deiconify()
        self.destroy()

    def out(self):
        """set the function of button start game and loads it"""
        app._master.deiconify()
        self.destroy()

def main():
    pass

if __name__ == "__main__":
    main()
    root = tk.Tk()
    app = LoadingScreen(root)
    root.mainloop()
