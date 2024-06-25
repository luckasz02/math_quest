import tkinter as tk
from models.student import Student
from tkinter import messagebox

class ParentDashboard:
    def __init__(self, root, parent, go_back_callback):
        self.root = root
        self.parent = parent
        self.go_back_callback = go_back_callback
        self.setup_ui()

    def setup_ui(self):
        self.clear_window()
        self.dashboard_label = tk.Label(self.root, text=f"Welcome, {self.parent['name']}", font=("Arial", 20))
        self.view_progress_button = tk.Button(self.root, text="View Children's Progress", font=("Arial", 16), command=self.view_progress)
        self.back_button = tk.Button(self.root, text="Back to Main Menu", font=("Arial", 16), command=self.go_back_callback)

        self.dashboard_label.pack(pady=10)
        self.view_progress_button.pack(pady=10)
        self.back_button.pack(pady=10)

    def view_progress(self):
        progress_text = ""
        for child_id in self.parent["children_ids"]:
            student = Student.get_student(child_id)
            if student:
                progress_text += f"Progress for {student['name']} (ID: {student['id']}):\n"
                if student["progress"]:
                    for entry in student["progress"]:
                        progress_text += f"  Quiz: {entry['quiz_name']}\n"
                        progress_text += f"  Total Score: {entry['total_score']}\n"
                        progress_text += f"  Test Score: {entry['test_score']}\n"
                        progress_text += f"  Time Taken: {entry.get('time_taken', 'N/A')} seconds\n"
                        progress_text += f"  Date: {entry['date']}\n\n"
                else:
                    progress_text += "  No progress recorded yet.\n\n"
            else:
                progress_text += f"No student found with ID: {child_id}\n\n"
        messagebox.showinfo("Children's Progress", progress_text)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
