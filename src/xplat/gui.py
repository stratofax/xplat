"""The GUI module for the xplat package."""
import tkinter as tk
import tkinter.ttk as ttk

from xplat import constants

PROGRAM_NAME = constants.PROGRAM_NAME
VERSION = constants.VERSION
APP_HELP = constants.APP_HELP
FONT = 'Arial'
BACKGROUND = 'white'
FOREGROUND = 'black'

WIDTH = 400
HEIGHT = 300


def start_gui() -> None:
    """Start the GUI."""
    window = tk.Tk()
    window.title(PROGRAM_NAME)
    window.geometry(f"{WIDTH}x{HEIGHT}")

    program_name = ttk.Label(window, text=PROGRAM_NAME,
                             font=(FONT, 20, 'bold'))
    program_name.pack(pady=20)

# Create a Label widget with center-aligned text
    app_help = ttk.Label(window, text=APP_HELP,
                         font=(FONT, 12, 'italic'),
                         )
    app_help.pack(padx=40)

    version = f"Version {VERSION}\n"
# Create a Text widget and add some initial text
    app_version = ttk.Label(window, text=version,
                            font=(FONT, 12),
                            justify='center')
    app_version.pack()

    window.mainloop()


if __name__ == "__main__":
    start_gui()
