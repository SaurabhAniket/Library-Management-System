# main.py
import tkinter as tk
from frontend import LibraryManagementApp

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()

