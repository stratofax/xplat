"""
Graphical User Interface (GUI) for xplat using Tkinter/ttk.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from . import info


class XplatGUI:
    """Main GUI window for xplat"""
    def __init__(self, root):
        self.root = root
        self.root.title("xplat")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.info_tab = self.create_info_tab()
        self.list_tab = self.create_list_tab()
        self.rename_tab = self.create_rename_tab()
        
        # Add tabs to notebook
        self.notebook.add(self.info_tab, text='Info')
        self.notebook.add(self.list_tab, text='List')
        self.notebook.add(self.rename_tab, text='Rename')
        
        # Initialize the info tab with system information
        self.update_info_display()

    def create_info_tab(self):
        """Create the Info tab with system information display"""
        frame = ttk.Frame(self.notebook)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # Create scrolled text widget for info display
        self.info_text = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=60,
            height=20
        )
        self.info_text.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Create refresh button
        refresh_btn = ttk.Button(
            frame,
            text="Refresh",
            command=self.update_info_display
        )
        refresh_btn.grid(row=1, column=0, pady=5)
        
        return frame

    def create_list_tab(self):
        """Create the List tab (placeholder for Phase 2)"""
        frame = ttk.Frame(self.notebook)
        ttk.Label(frame, text="File listing feature coming soon...").pack(padx=20, pady=20)
        return frame

    def create_rename_tab(self):
        """Create the Rename tab (placeholder for Phase 3)"""
        frame = ttk.Frame(self.notebook)
        ttk.Label(frame, text="File renaming feature coming soon...").pack(padx=20, pady=20)
        return frame

    def update_info_display(self):
        """Update the info display with current system information"""
        self.info_text.delete('1.0', tk.END)
        platform_info = info.create_platform_report()
        self.info_text.insert('1.0', platform_info)
        self.info_text.config(state='disabled')  # Make read-only


def main():
    """Main entry point for the GUI"""
    root = tk.Tk()
    root.geometry("600x500")  # Set initial window size
    app = XplatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
