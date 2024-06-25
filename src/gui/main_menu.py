import tkinter as tk
from tkinter import ttk
from gui.children_portal import ChildrenPortal
from gui.teacher_portal import TeacherPortal
from gui.parent_portal import ParentPortal

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.clear_window()  # Clear previous UI elements first
        self.root.title("MathQuest")
        self.root.geometry("600x400")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')

        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="MathQuest: A Fun Math Adventure", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        student_button = ttk.Button(button_frame, text="Children's Portal", command=self.open_children_portal)
        student_button.pack(side=tk.LEFT, padx=10)

        teacher_button = ttk.Button(button_frame, text="Teacher's Portal", command=self.open_teacher_portal)
        teacher_button.pack(side=tk.LEFT, padx=10)

        parent_button = ttk.Button(button_frame, text="Parent's Portal", command=self.open_parent_portal)
        parent_button.pack(side=tk.LEFT, padx=10)

    def open_children_portal(self):
        self.clear_window()
        ChildrenPortal(self.root, self.show_main_menu)

    def open_teacher_portal(self):
        self.clear_window()
        TeacherPortal(self.root, self.show_main_menu)

    def open_parent_portal(self):
        self.clear_window()
        ParentPortal(self.root, self.show_main_menu)

    def show_main_menu(self):
        self.setup_ui()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
