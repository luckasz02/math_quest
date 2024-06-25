import tkinter as tk
from tkinter import messagebox
from models.teacher import Teacher
from gui.teacher_dashboard import TeacherDashboard

class TeacherPortal:
    def __init__(self, root, go_back_callback):
        self.root = root
        self.go_back_callback = go_back_callback
        self.setup_ui()

    def setup_ui(self):
        self.clear_window()
        self.login_label = tk.Label(self.root, text="Teacher Login", font=("Arial", 20))
        self.username_label = tk.Label(self.root, text="Username:", font=("Arial", 16))
        self.password_label = tk.Label(self.root, text="Password:", font=("Arial", 16))
        self.username_entry = tk.Entry(self.root, font=("Arial", 16))
        self.password_entry = tk.Entry(self.root, font=("Arial", 16), show="*")
        self.login_button = tk.Button(self.root, text="Login", font=("Arial", 16), command=self.check_teacher_login)
        self.signup_button = tk.Button(self.root, text="Sign Up", font=("Arial", 16), command=self.teacher_signup)
        self.back_button = tk.Button(self.root, text="Back to Main Menu", font=("Arial", 16), command=self.go_back_callback)

        self.login_label.pack(pady=10)
        self.username_label.pack(pady=5)
        self.username_entry.pack(pady=5)
        self.password_label.pack(pady=5)
        self.password_entry.pack(pady=5)
        self.login_button.pack(pady=5)
        self.signup_button.pack(pady=5)
        self.back_button.pack(pady=10)

    def teacher_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if Teacher.exists(username):
            messagebox.showerror("Error", "Username already exists")
        else:
            Teacher.create(username, password)
            messagebox.showinfo("Success", "Account created successfully")
            self.go_back_callback()

    def check_teacher_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if Teacher.authenticate(username, password):
            self.clear_window()
            TeacherDashboard(self.root, username, self.go_back_callback)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
