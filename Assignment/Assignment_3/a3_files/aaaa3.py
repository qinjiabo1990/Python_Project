"""
CSSE1001 Assignment 3
Semester 1, 2017
"""
import tkinter.ttk as ttk#
import tkinter as tk#
from tkinter import filedialog
from tkinter import messagebox#
import model#
import view#
from game_lucky7 import Lucky7Game#
from game_make13 import Make13Game#
from game_regular import RegularGame#
from game_unlimited import UnlimitedGame#
from base import BaseLoloApp#
import random#
from highscores import HighScoreManager#

__author__ = "Yishen Zhang"
__email__ = "yishen.zhang@uq.edu.au"
__version__ = "1.0.3"


# Define your classes here
class LoloApp(BaseLoloApp):

    def __init__(self, master, game=Make13Game(goal_value=13), grid_view=None):

        super().__init__(master, game, grid_view)
        self._grid_view.pack_forget()

        self._master.configure(bg="gray90")
        self._master.title("Lolo :: " + self._game.get_name() + " Game")
        self._master.minsize(500, 700)

        self.create_menu()

        self.create_logo_frame()
        
        self.canvas = LoloLogo(self.logo_frame)

        self.status_bar = StatusBar(self.logo_frame, self._game)

        self._grid_view.configure(bg=self._master.cget("bg"))
        self._grid_view.pack(side=tk.TOP, expand=False)

        self.create_lightning()

    def create_menu(self):
        self.menubar = tk.Menu(self._master)
        self._master.config(menu=self.menubar)
        self.filemenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.selections = [("New Game",self.reset),
                           ("High Scores",self.open_high_score_window),
                           ("Exit",self.exit)]
        for selection, cmd in self.selections:
            self.filemenu.add_command(label=selection, command=cmd)
        self._master.bind("<Control-n>", self.reset)

    def create_logo_frame(self):
        self.logo_frame = tk.Frame(self._master, width=500, bg=self._master.cget("bg"))
        self.logo_frame.pack(side=tk.TOP)
        
    def create_lightning(self):
        self.round_counter = 0
        self.lightning_chances = 1
        self.lightning_button = tk.Button(self._master, text="lightning: "+str(self.lightning_chances),
                                          fg="green", command=self.lightning_using)
        self.lightning_button.pack(side=tk.TOP, pady=10)
        self._master.bind("<Control-l>", self.lightning_using)

    def lightning_reward(self):
        self.round_counter += 1
        if self.round_counter >= 3:
            self.lightning_chances += 1
            self.round_counter = 0
            self.lightning_button.configure(text="lightning: "+str(self.lightning_chances))
                                            
    def lightning_using(self):
        if self.lightning_chances > 0:
            self.lightning_button.configure(text="choose a tile to delete",
                                            fg="yellow", bg="black")
            self._grid_view.off('select', self.activate)
            self._grid_view.on('select', self.remove)
        else :
            messagebox.showwarning(title="Not enough lightning",
                            message="No more chance for cheating!")
            
    def lightning_used(self):
        self.lightning_chances -= 1
        self._grid_view.off('select', self.remove)
        self._grid_view.on('select', self.activate)
        self.lightning_button.configure(text="lightning: "+str(self.lightning_chances),
                                        fg="green", bg="gray90")
        self._master.after(200, self.game_over)
        
    def open_high_score_window(self):
        self.new_window = tk.Toplevel(self._master)
        self.app = HighScoreWindow(self.new_window)
        
    def bind_events(self):
        super().bind_events()
        self._game.on('score', self.set_score)
        
    def activate(self, position):
        """Attempts to activate the tile at the given position.

        Parameters:
            position (tuple<int, int>): Row-column position of the tile.

        Raises:
            IndexError: If position cannot be activated.
        """
        # Magic. Do not touch.
        if position is None:
            return

        if self._game.is_resolving():
            return
        
        if position in self._game.grid:

            if not self._game.can_activate(position):
                return messagebox.showinfo(title="Wrong Tile",
                                           message="This tile can't be activated!")
            else :
                self.lightning_reward()
                
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
            self.lightning_used()
            
        def draw_grid():
            self._grid_view.draw(self._game.grid)

        animation = self.create_animation(self._game.remove(*positions),
                                          func=draw_grid,
                                          callback=finish_move)
        animation()

    def reset(self, ev=None):#good
        self._game.reset()
        self._game.set_score(0)
        self._grid_view.draw(self._game.grid, self._game.find_connections())
        self.lightning_chances = 1
        
    def exit(self):#good
        exit()

    def set_game(self):
        self._mode_label.configure(text=self._game.get_name()+" Game")
        
    def set_score(self, points):
        self.status_bar._score_label.configure(text="Score: {}".format(self._game.get_score()))
     
    def game_over(self):
        if self.lightning_chances <= 0 and self._game.game_over():
            return messagebox.showwarning(title="Game Over",
                                          message="No mercy for stooges!")

class StatusBar(tk.Frame):

    def __init__(self, master, game):
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

    def __init__(self, master):
        super().__init__(master)
        self._master = master
        self.configure(width=500, height=120,
                       bg=self._master.cget("bg"),
                       highlightthickness=0, relief='ridge')
        self.pack(side=tk.TOP)
        self.drawlogo()
        
    # 34 30 4 30 4 30 4 30 34
    def drawlogo(self):
        self.create_polygon([(95,10),(95,110),(165,110),(165,87),
                             (118,87),(118,10)], fill="purple4",outline="")
        self.create_oval([(175,40),(245,110)], fill="purple4", outline="")
        self.create_oval([(198,63),(222,87)], fill=self._master.cget("bg"), outline="")
        self.create_polygon([(255,10),(255,110),(325,110),(325,87),
                             (278,87),(278,10)], fill="purple4",outline="")
        self.create_oval([(335,40),(405,110)], fill="purple4", outline="")
        self.create_oval([(358,63),(382,87)], fill=self._master.cget("bg"), outline="")
"""-----------------------------------------------------------------------------"""
class  AutoPlayingGame(BaseLoloApp):

    def __init__(self, master, game=None, grid_view=None):
        super().__init__(master, game, grid_view)
        self._grid_view.pack_forget()
        self._grid_view.configure(bg=self._master.cget("bg"))
        self._grid_view.pack()
        
        self.activate(self.new_position())

    def bind_events(self):
        """Binds relevant events."""
        self._grid_view.on('select', self.activate)
        self._game.on('game_over', self.game_over)
        self._game.on('score', self.score)

    def new_position(self):
        j=[]
        for valid_positions in self._game.find_groups():
            j.append(valid_positions)
        i=int(len(j)*random.random())
        if len(j):
            return j[i].pop()

    def activate(self, position):
        """Attempts to activate the tile at the given position.

        Parameters:
            position (tuple<int, int>): Row-column position of the tile.

        Raises:
            IndexError: If position cannot be activated.
        """
        # Magic. Do not touch.
        if position is None:
            return

        if self._game.is_resolving():
            return

        if position in self._game.grid:
            
            def finish_move():
                self._grid_view.draw(self._game.grid,
                                     self._game.find_connections())
                self._master.after(200,self.activate(self.new_position()))
                
            def draw_grid():
                self._grid_view.draw(self._game.grid)

            animation = self.create_animation(self._game.activate(position),
                                              func=draw_grid,
                                              callback=finish_move)
            animation()

    def reset(self):
        self._game.reset()
        self._game.set_score(0)
        self._grid_view.draw(self._game.grid, self._game.find_connections())
        self.activate(self.new_position())
        
    def game_over(self):
        self._master.after(200, self.reset)

    def exit(self):
        exit()
               
class LoadingScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self._master = master
        self._master.title("Lolo")
        self._master.configure(bg="gray60")
        self._master.minsize(700, 700)
        
        self.configure(bg=self._master.cget("bg"))
        self.pack(side=tk.TOP)

        self.canvas = LoloLogo(self)

        style = ttk.Style()
        style.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])
        
        self.create_entry_frame()

        self.create_autoplay()

        self.create_selection_frame()

    def create_entry_frame(self):
        self.entry_frame = tk.Frame(self, bg=self.cget("bg"))
        self.entry_frame.pack(side=tk.TOP, pady=10)
        
        self.entry_label = tk.Label(self.entry_frame, text="Your Name : ",
                                    bg=self.cget("bg"), fg="white")
        self.entry_label.pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.entry_frame)
        self.name_entry.pack(side=tk.LEFT)
        
    def create_autoplay(self):
        self.autoplay_frame = tk.Frame(self, bg=self.cget("bg"))
        self.autoplay_frame.pack(side=tk.RIGHT, expand=True)
        self.autoplay = AutoPlayingGame(self.autoplay_frame)

    def create_selection_frame(self):
        self.selection_frame = tk.Frame(self, bg=self.cget("bg"))
        self.selection_frame.pack(side=tk.LEFT, padx=50, expand=True)

        self._options = [("Play Game", self.start_play),
                         ("Game Modes", self.show_modes),
                         ("High Score", None),
                         ("Exit Game", self._master.destroy)]
        for option, cmd in  self._options:
            button = ttk.Button(self.selection_frame, text=option,command=cmd)
            button.pack(side=tk.TOP, pady=50, ipadx=150)
            
    def start_play(self):
        if len(self.name_entry.get()):
            loading_app.pack_forget()
            loading_app.destroy()
            game_app = LoloApp(root)
        else:
            messagebox.showwarning(title="Player name",
                                   message="Please entry your name before play the game.")

    def show_modes(self):
        if len(self.name_entry.get()):
            loading_app._master.wm_withdraw()
            self._pause = True
            self.gamemodes_window = GameModes()
        else:
            messagebox.showwarning(title="Player name",
                                   message="Please entry your name before play the game.")
        
class GameModes(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.configure(bg="gray90")
        
        self.selections_frame = tk.Frame(self, bg=self.cget("bg"))
        self.selections_frame.pack(side=tk.TOP, expand=True)

        self.create_game_options()

        self.create_autoplay(game=self.get_modes())

        self.create_bottom_buttons()

    def create_game_options(self):
        self.v = tk.StringVar()
        self.v.set("regular")
        self._modes = [("Lucky 7 Game", "lucky7"),
                       ("Make 13 Game", "make13"),
                       ("Regular Game", "regular"),
                       ("Unlimited Game", "unlimited")]
        for modename, gamecode in  self._modes:
            button = tk.Radiobutton(self.selections_frame, bg=self.cget("bg"),
                                    variable=self.v, text=modename,
                                    value=gamecode, command=self.set_autoplay)
            button.pack(side=tk.LEFT)
    
    def create_autoplay(self, game):
        if game == None:
            game = RegularGame(types=3)
        self.autoplay_frame = tk.Frame(self,
                                        bg=self.cget("bg"))
        self.autoplay_frame.pack(side=tk.TOP, expand=True)
        self.autoplay = AutoPlayingGame(self.autoplay_frame, game=game)
    
    def create_bottom_buttons(self):
        self.button_frame = tk.Frame(self, bg=self.cget("bg"))
        self.button_frame.pack(side=tk.TOP)

        self._options =[("Play Game", self.start_play),
                        ("Cancel", self.quit)]
        for option, cmd in self._options:
            button = tk.Button(self.button_frame, text=option,
                               bg=self.cget("bg"), command=cmd)
            button.pack(side=tk.LEFT, padx=5, pady=10)
        
    def get_modes(self):
        self.game_codes = {"regular": RegularGame(types=3),
                       "make13": Make13Game(goal_value=13),
                       "lucky7": Lucky7Game(lucky_value=7),
                       "unlimited": UnlimitedGame(types=4)}
        if self.v.get():
            return self.game_codes[self.v.get()]
        else:
            return RegularGame(types=3)

    def set_autoplay(self):
        self.autoplay_frame.destroy()
        self.button_frame.pack_forget()
        self.create_autoplay(self.get_modes())
        self.button_frame.pack()

    def start_play(self):
        loading_app.destroy()
        game_app = LoloApp(root, game=self.get_modes())
        game_app._master.deiconify()
        self.destroy()
            
    def quit(self):
        loading_app._master.deiconify()
        self.destroy()

class HighScoreWindow:

    def __init__(self, master):
        self._master = master
        self._master.title("High Scores :: Lolo")
        self._frame = tk.Frame(self._master)
        self._frame.pack(side=tk.TOP)
        self._text = tk.Text(self._frame)
        self._text.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.high_score_manager = HighScoreManager(file="highscores.json", gamemode='regular',
                                                   auto_save=True, top_scores=10)
        fd = self.high_score_manager.get_sorted_data()
        self._text.insert(tk.INSERT, fd)


def main():
    pass
    # Your GUI instantiation code here


if __name__ == "__main__":
    root = tk.Tk()
    loading_app = LoadingScreen(root)
    #game_app = LoloApp(root)
    #game_app = AutoPlayingGame(root)
    #game_app = LoadingScreen(root)
    root.mainloop()
    #Lucky7Game(lucky_value=7)
    #Make13Game(goal_value=13)
    #RegularGame(types=3)
    #UnlimitedGame(types=4)
