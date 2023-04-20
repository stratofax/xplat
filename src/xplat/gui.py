"""The GUI module for the xplat package."""
import tkinter as tk

from xplat import constants

PROGRAM_NAME = constants.PROGRAM_NAME
VERSION = constants.VERSION
APP_HELP = constants.APP_HELP
FONT = 'Arial'
BACKGROUND = 'white'
FOREGROUND = 'black'


class XplatStart(tk.Tk):
    """The main application class for the xplat package."""
    def __init__(self):
        """Initialize the application."""
        WIDTH = 400
        HEIGHT = 300
        super().__init__()
        self.title(PROGRAM_NAME)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.configure(bg=BACKGROUND)

        program_name = tk.Label(self, text=PROGRAM_NAME,
                                font=(FONT, 20, 'bold'),
                                bg=BACKGROUND, fg=FOREGROUND)
        program_name.pack(pady=20)

        # Create a Label widget with center-aligned text
        app_help = tk.Label(self, text=APP_HELP,
                            font=(FONT, 12, 'italic'),
                            bg=BACKGROUND, fg=FOREGROUND,
                            width=40, height=3, wraplength=WIDTH*0.8,
                            justify='center')
        app_help.pack()

        version = f"Version {VERSION}\n"
        # Create a Text widget and add some initial text
        app_version = tk.Label(self, text=version,
                               font=(FONT, 12), bg=BACKGROUND, fg=FOREGROUND,
                               width=40, height=3, wraplength=WIDTH*0.8,
                               justify='center')
        app_version.pack()


def start_gui() -> None:
    """Start the GUI."""
    app = XplatStart()
    app.mainloop()


if __name__ == "__main__":
    start_gui()
