import tkinter as tk
from tkinter import simpledialog, messagebox
from models.quiz import Quiz
from models.student import Student

class TeacherDashboard:
    def __init__(self, root, username, go_back_callback):
        self.root = root
        self.username = username
        self.go_back_callback = go_back_callback
        self.setup_ui()

    def setup_ui(self):
        self.clear_window()
        self.dashboard_label = tk.Label(self.root, text=f"Welcome, {self.username}", font=("Arial", 20))
        self.add_quiz_button = tk.Button(self.root, text="Create New Quiz", font=("Arial", 16), command=self.create_quiz)
        self.add_question_button = tk.Button(self.root, text="Add Question to Quiz", font=("Arial", 16), command=self.add_question)
        self.view_quizzes_button = tk.Button(self.root, text="View Quizzes", font=("Arial", 16), command=self.view_quizzes)
        self.add_student_button = tk.Button(self.root, text="Add Student", font=("Arial", 16), command=self.add_student)
        self.view_students_button = tk.Button(self.root, text="View Students", font=("Arial", 16), command=self.view_students)
        self.view_student_progress_button = tk.Button(self.root, text="View Student Progress", font=("Arial", 16), command=self.view_student_progress)
        self.back_button = tk.Button(self.root, text="Back to Main Menu", font=("Arial", 16), command=self.go_back_callback)

        self.dashboard_label.pack(pady=10)
        self.add_quiz_button.pack(pady=5)
        self.add_question_button.pack(pady=5)
        self.view_quizzes_button.pack(pady=5)
        self.add_student_button.pack(pady=5)
        self.view_students_button.pack(pady=5)
        self.view_student_progress_button.pack(pady=5)
        self.back_button.pack(pady=10)

    def create_quiz(self):
        quiz_name = simpledialog.askstring("Input", "Enter the quiz name:")
        if quiz_name:
            Quiz.create_quiz(quiz_name)
            messagebox.showinfo("Success", f"Quiz '{quiz_name}' created successfully")

    def add_question(self):
        quiz_name = simpledialog.askstring("Input", "Enter the quiz name to add a question:")
        if not Quiz.exists(quiz_name):
            messagebox.showerror("Error", f"Quiz '{quiz_name}' does not exist")
            return
        level = simpledialog.askstring("Input", "Enter the level for the question (1, 2, 3, 4, or Test):")
        if level.lower() == "test":
            Quiz.create_test_level(quiz_name)
            messagebox.showinfo("Success", "Test level created with random questions from all levels.")
        else:
            question = simpledialog.askstring("Input", "Enter the question:")
            answer = simpledialog.askstring("Input", "Enter the answer:")
            hint = simpledialog.askstring("Input", "Enter a hint:")
            Quiz.add_question(quiz_name, level, question, answer, hint)
            messagebox.showinfo("Success", "Question added successfully")

    def view_quizzes(self):
        quizzes = Quiz.get_all_quizzes()
        if quizzes:
            quiz_text = ""
            for quiz_name, quiz_data in quizzes.items():
                quiz_text += f"Quiz '{quiz_name}':\n"
                for level, questions in quiz_data["levels"].items():
                    quiz_text += f"  Level {level}:\n"
                    quiz_text += "\n".join([f"    Q: {q['question']}\n    A: {q['answer']}\n    Hint: {q['hint']}" for q in questions])
                    quiz_text += "\n"
                quiz_text += "\n"
            messagebox.showinfo("Quizzes", quiz_text)
        else:
            messagebox.showinfo("Quizzes", "No quizzes available")

    def add_student(self):
        student_name = simpledialog.askstring("Input", "Enter the student's name:")
        student_id = simpledialog.askstring("Input", "Enter the student's ID:")
        
        Student.add_student(student_name, student_id)
        messagebox.showinfo("Success", "Student added successfully")

    def view_students(self):
        students = Student.get_all_students()
        if students:
            student_text = "\n".join([f"ID: {s['id']}\nName: {s['name']}" for s in students])
            messagebox.showinfo("Students", student_text)
        else:
            messagebox.showinfo("Students", "No students available")

    def view_student_progress(self):
        student_id = simpledialog.askstring("Input", "Enter the student's ID:")
        student = Student.get_student(student_id)
        if student:
            progress_text = f"Progress for {student['name']} (ID: {student['id']}):\n\n"
            if student["progress"]:
                for entry in student["progress"]:
                    progress_text += f"Quiz: {entry['quiz_name']}\n"
                    progress_text += f"Total Score: {entry['total_score']}\n"
                    progress_text += f"Test Score: {entry['test_score']}\n"
                    progress_text += f"Time Taken: {entry.get('time_taken', 'N/A')} seconds\n"
                    progress_text += f"Date: {entry['date']}\n\n"
            else:
                progress_text += "No progress recorded yet."
            messagebox.showinfo("Student Progress", progress_text)
        else:
            messagebox.showerror("Error", "Student not found")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
