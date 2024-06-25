import tkinter as tk
import random
from tkinter import messagebox
import json
import os
from models.student import Student
from datetime import datetime

class ChildrenPortal:
    def __init__(self, root, go_back_callback):
        self.root = root
        self.go_back_callback = go_back_callback
        self.quizzes_file = os.path.join(os.path.dirname(__file__), '../../data/quizzes.json')

        self.student = None
        self.load_quizzes()
        self.show_login_screen()

    def load_quizzes(self):
        if os.path.exists(self.quizzes_file):
            with open(self.quizzes_file, 'r') as f:
                self.quizzes = json.load(f)
        else:
            self.quizzes = {}
        print("Quizzes loaded:", self.quizzes)

    def show_login_screen(self):
        self.clear_window()
        self.login_label = tk.Label(self.root, text="Login to MathQuest", font=("Arial", 20))
        self.name_label = tk.Label(self.root, text="Full Name:", font=("Arial", 16))
        self.name_entry = tk.Entry(self.root, font=("Arial", 16))
        self.id_label = tk.Label(self.root, text="Student ID:", font=("Arial", 16))
        self.id_entry = tk.Entry(self.root, font=("Arial", 16))
        self.login_button = tk.Button(self.root, text="Login", font=("Arial", 16), command=self.login)
        self.back_button = tk.Button(self.root, text="Back to Main Menu", font=("Arial", 16), command=self.go_back_callback)

        self.login_label.pack(pady=20)
        self.name_label.pack()
        self.name_entry.pack(pady=5)
        self.id_label.pack()
        self.id_entry.pack(pady=5)
        self.login_button.pack(pady=20)
        self.back_button.pack(pady=10)

    def login(self):
        name = self.name_entry.get()
        student_id = self.id_entry.get()
        students = Student.get_all_students()
        for student in students:
            if student["name"] == name and student["id"] == student_id:
                self.student = student
                self.select_quiz()
                return
        messagebox.showerror("Login Failed", "Invalid name or student ID")

    def select_quiz(self):
        self.clear_window()
        self.quiz_label = tk.Label(self.root, text=f"Welcome {self.student['name']}, Select a Quiz", font=("Arial", 20))
        self.quiz_label.pack(pady=10)
        for quiz_name in self.quizzes:
            quiz_button = tk.Button(self.root, text=quiz_name, font=("Arial", 16), command=lambda q=quiz_name: self.start_quiz(q))
            quiz_button.pack(pady=5)
        self.back_button = tk.Button(self.root, text="Back to Main Menu", font=("Arial", 16), command=self.go_back_callback)
        self.back_button.pack(pady=10)

    def start_quiz(self, quiz_name):
        print(f"Starting quiz: {quiz_name}")
        self.quiz_name = quiz_name
        self.levels = sorted([level for level in self.quizzes[quiz_name]["levels"].keys() if level.lower() != "test"], key=int)
        self.is_test_level = "Test" in self.quizzes[quiz_name]["levels"]
        print(f"Levels for quiz {quiz_name}:", self.levels)
        self.current_level_index = 0
        self.total_score = 0  
        self.test_score = 0  
        self.score = 0  
        self.current_question = 0
        self.level_score = 0
        self.required_score_to_advance = {1: 3, 2: 3, 3: 4}
        self.time_left = 60
        self.timer = None
        self.questions = []
        self.start_time = None  
        self.setup_ui()
        self.start_level()

    def start_level(self):
        if self.is_test_level and self.current_level_index == len(self.levels):
            messagebox.showinfo("Total Score", f"Your total score from levels: {self.total_score}/{sum(self.required_score_to_advance.values())}")
            self.prepare_test_level()
            self.current_level = "Test"
            self.time_left = 60  
            self.start_time = datetime.now()  
            messagebox.showinfo("Test Level", "You have entered the test level. The timer has started.")
            self.start_timer()  
        else:
            self.current_level = self.levels[self.current_level_index]
        print(f"Starting level: {self.current_level}")
        self.questions = self.quizzes[self.quiz_name]["levels"][self.current_level]
        self.current_question = 0
        self.level_score = 0  
        self.update_score_label()
        messagebox.showinfo("Level Up!", f"Welcome to Level {self.current_level}!")
        self.display_next_question()

    def prepare_test_level(self):
        questions = []
        for level in self.levels:
            questions.extend(self.quizzes[self.quiz_name]["levels"][level])
        random.shuffle(questions)
        self.questions = questions[:10]

    def setup_ui(self):
        self.clear_window()
        self.root.configure(bg='#f0f8ff')
        
        self.question_label = tk.Label(self.root, text="", font=("Arial", 20, "bold"), bg='#f0f8ff', fg='#333')
        self.entry = tk.Entry(self.root, font=("Arial", 16), bd=3, relief="ridge")
        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_answers, font=("Arial", 14, "bold"), bg='#87cefa', fg='white', bd=3, relief="raised")
        self.hint_button = tk.Button(self.root, text="Hint", command=self.show_hint, font=("Arial", 14, "bold"), bg='#ffa07a', fg='white', bd=3, relief="raised")
        self.score_label = tk.Label(self.root, text="Score: 0/0", font=("Arial", 16), bg='#f0f8ff', fg='#333')
        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left}s", font=("Arial", 16), bg='#f0f8ff', fg='#333')
        self.retry_button = tk.Button(self.root, text="Retry Level", command=self.retry_level, font=("Arial", 14, "bold"), bg='#ff6347', fg='white', bd=3, relief="raised")
        self.retry_test_button = tk.Button(self.root, text="Retry Test", command=self.retry_test, font=("Arial", 14, "bold"), bg='#ff6347', fg='white', bd=3, relief="raised")
        self.back_button = tk.Button(self.root, text="Back to Main Menu", font=("Arial", 14, "bold"), bg='#87cefa', fg='white', bd=3, relief="raised", command=self.go_back_callback)

        self.question_label.pack(pady=(20, 10))
        self.entry.pack(pady=(0, 20))
        self.submit_button.pack(pady=(0, 10))
        self.hint_button.pack(pady=(0, 20))
        self.score_label.pack(pady=(0, 10))
        self.timer_label.pack(pady=(0, 20))
        self.retry_button.pack(pady=(0, 10))
        self.retry_test_button.pack(pady=(0, 10))
        self.back_button.pack(pady=(0, 10))

        self.root.bind('<Return>', self.check_answers_event)

    def display_next_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data["question"])
            self.current_question += 1
        else:
            if self.current_level == "Test":
                self.end_game()
            elif self.level_score >= self.required_score_to_advance.get(int(self.current_level), 0):
                self.total_score += self.level_score  
                self.current_level_index += 1
                if self.current_level_index >= len(self.levels) and not self.is_test_level:
                    self.end_game()
                else:
                    self.start_level()
            else:
                messagebox.showinfo("Try Again", f"You need at least {self.required_score_to_advance.get(int(self.current_level), 0)} correct answers to advance. Please try again.")

    def check_answers(self):
        user_answer = self.entry.get()
        correct_answer = self.questions[self.current_question - 1]["answer"]
        if user_answer == correct_answer:
            self.score += 1
            self.level_score += 1 if self.current_level != "Test" else 0
            self.test_score += 1 if self.current_level == "Test" else 0
        self.entry.delete(0, 'end')
        self.update_score_label()
        self.display_next_question()

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}/{sum(len(self.quizzes[self.quiz_name]['levels'][level]) for level in self.levels)}")

    def check_answers_event(self, event):
        self.check_answers()

    def show_hint(self):
        hint = self.questions[self.current_question - 1]["hint"]
        messagebox.showinfo("Hint", hint)

    def retry_level(self):
        self.level_score = 0
        self.current_question = 0
        self.score = 0  
        self.update_score_label()
        self.display_next_question()

    def retry_test(self):
        self.test_score = 0
        self.current_question = 0
        self.score = 0  
        self.time_left = 60 
        if self.timer:
            self.root.after_cancel(self.timer)  
        self.start_time = datetime.now()  
        messagebox.showinfo("Test Level", "You have entered the test level. The timer has started.")
        self.update_score_label()
        self.start_level()

    def end_game(self):
        total_possible_score = sum(len(self.quizzes[self.quiz_name]['levels'][level]) for level in self.levels)
        time_taken = (datetime.now() - self.start_time).total_seconds() if self.start_time else None
        self.question_label.config(text=f"Game Over! Your total score: {self.total_score}/{total_possible_score}\nTest score: {self.test_score}/10")
        self.entry.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.hint_button.config(state="disabled")
        if self.timer:
            self.root.after_cancel(self.timer)
        Student.add_progress(self.student["id"], self.quiz_name, self.total_score, self.test_score, time_taken)
        messagebox.showinfo("Game Over", f"Congratulations! You've completed the quiz with a total score of {self.total_score}/{total_possible_score} and a test score of {self.test_score}/10\nTime taken: {time_taken:.2f} seconds")

    def start_timer(self):
        if self.timer:
            self.root.after_cancel(self.timer)
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.timer = self.root.after(1000, self.start_timer)
        else:
            self.end_game()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
