"""Solutions to the week 9 tutorial questions
about GUI component layout and simple event handling.
zq
__copyright__ = "Copyright 2017, University of Queensland"
"""

import tkinter as tk
from tkinter import messagebox


class SampleApp(object) :
    def __init__(self, master) :
        self._master = master
        master.title("Hello!")
        master.minsize(430, 200)

        self._label = tk.Label(master, text="Choose a button")
        # We want the label to stay roughly in the centre when the window is
        # resized, so we use expand, which will claim as much space in all
        # directions as possible. This will keep the label centred, because
        # widgets automatically stay to the centre of all the space that is
        # available to them.
        self._label.pack(side=tk.TOP, expand=True)

        # To get the buttons to stay horizontally centred and aligned to the
        # bottom of the window, we created a button frame and align the buttons
        # within it, and apply any alignments we want for the group of buttons
        # collectively to the frame.
        button_frame = tk.Frame(master)
        button_frame.pack(side=tk.TOP)
        # When this button is clicked, the label colour should change to blue.
        button = tk.Button(button_frame, text="Change to Blue",
                           command=self.change_blue)
        button.pack(side=tk.LEFT)
        # When this button is clicked, the label colour should change to green.
        button = tk.Button(button_frame, text="Change to Green",
                           command=self.change_green)
        button.pack(side=tk.LEFT)

        entry_frame = tk.Frame(master)
        entry_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        entry_label = tk.Label(entry_frame, text="Change the colour to: ")
        entry_label.pack(side=tk.LEFT)
        self._colour_entry = tk.Entry(entry_frame)
        self._colour_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        # When this button is clicked, the label colour should change to the
        # colour that the user has entered.
        change_button = tk.Button(entry_frame, text="Change it!",
                                  command=self.change)
        change_button.pack(side=tk.LEFT)

    def change_blue(self) :
        """Changes the colour of the label to blue."""
        self._label.config(text="This label is blue", bg="blue")

    def change_green(self) :
        """Changes the colour of the label to green."""
        self._label.config(text="This label is green", bg="green")

    def change(self) :
        """Changes the colour of the label to whatever the user has entered.
           Shows an error box if the user has entered an invalid colour.
        """
        # Get the text that the user has entered in the colour entry.
        colour = self._colour_entry.get()
        try :
            # Try to set the colour.
            # Raises a TclError if the colour is invalid
            self._label.config(text="This label is " + colour, bg=colour)
        except tk.TclError :
            # If the user had entered an invalid colour, prompt them.
            messagebox.showerror("Invalid colour",
                                   "'" + colour + "' is not a colour!")


if __name__ == "__main__" :
    root = tk.Tk()
    app = SampleApp(root)
    root.mainloop()
