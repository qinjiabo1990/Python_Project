import tkinter as tk
from tkinter import messagebox

class LoloLogo(tk.Canvas):
    def __init__(self, master):
        super().__init__(master)
        master.title("Lolo :: {game_mode_name} Game")
        #master.geometry("400x400")

        self._canvas = tk.Canvas(master, bg="white", width=600, height=700)
        self._canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._canvas.create_rectangle(120,20,140,90, fill= "#6d4876", outline="#6d4876")
        self._canvas.create_rectangle(120,90,180,110, fill= "#6d4876", outline="#6d4876")
        self._canvas.create_oval(210, 40, 270, 100, outline="#6d4876", width=20)
        self._canvas.create_rectangle(310,20,330,90, fill= "#6d4876", outline="#6d4876")
        self._canvas.create_rectangle(310,90,370,110, fill= "#6d4876", outline="#6d4876")
        self._canvas.create_oval(400, 40, 460, 100, outline="#6d4876", width=20)

class StatusBar(tk.Frame):
    def __int__(self, master):
        super().__init__(master)
        mode = tk.Label(self, text="Regular Mode") #need to modify
        mode.pack(side=tk.LEFT)
        score = tk.Label(self, text="Score:")
        score.pack(side=tk.RIGHT)

    
root = tk.Tk()
app = LoloLogo(root)
root.mainloop()
