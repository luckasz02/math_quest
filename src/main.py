from gui.main_menu import MainMenu
from models.student import Student

import tkinter as tk

Student.update_progress_with_default_time()

root = tk.Tk()
root.title("MathQuest")
main_menu = MainMenu(root)
root.mainloop()
