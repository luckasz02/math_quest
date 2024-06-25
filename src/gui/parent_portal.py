import tkinter as tk
from tkinter import simpledialog, messagebox
from models.parent import Parent
from gui.parent_dashboard import ParentDashboard

class ParentPortal:
    def __init__(self, root, go_back_callback):
        self.root = root
        self.go_back_callback = go_back_callback
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_window()
        self.login_label = tk.Label(self.root, text="Parent Login", font=("Arial", 20))
        self.name_label = tk.Label(self.root, text="Full Name:", font=("Arial", 16))
        self.name_entry = tk.Entry(self.root, font=("Arial", 16))
        self.id_label = tk.Label(self.root, text="Parent ID:", font=("Arial", 16))
        self.id_entry = tk.Entry(self.root, font=("Arial", 16))
        self.login_button = tk.Button(self.root, text="Login", font=("Arial", 16), command=self.login)
        self.signup_button = tk.Button(self.root, text="Signup", font=("Arial", 16), command=self.signup)
        self.back_button = tk.Button(self.root, text="Back to Main Menu", font=("Arial", 16), command=self.go_back_callback)

        self.login_label.pack(pady=20)
        self.name_label.pack()
        self.name_entry.pack(pady=5)
        self.id_label.pack()
        self.id_entry.pack(pady=5)
        self.login_button.pack(pady=10)
        self.signup_button.pack(pady=10)
        self.back_button.pack(pady=10)

    def login(self):
        name = self.name_entry.get()
        parent_id = self.id_entry.get()
        parents = Parent.get_all_parents()
        for parent in parents:
            if parent["name"] == name and parent["id"] == parent_id:
                self.parent = parent
                self.open_dashboard()
                return
        messagebox.showerror("Login Failed", "Invalid name or parent ID")

    def signup(self):
        name = self.name_entry.get()
        parent_id = self.id_entry.get()
        children_ids = simpledialog.askstring("Input", "Enter the children's IDs, separated by commas:").split(',')
        Parent.add_parent(name, parent_id, children_ids)
        messagebox.showinfo("Signup Success", "Parent account created successfully")
        self.login()

    def open_dashboard(self):
        self.clear_window()
        ParentDashboard(self.root, self.parent, self.go_back_callback)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
