"""
main.py
-------
Run this file to start the Fitness Performance Analytics System.
"""

import tkinter as tk

from gui import FitnessApp


def main():
    root = tk.Tk()
    FitnessApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
