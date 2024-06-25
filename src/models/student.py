import json
import os
from datetime import datetime

class Student:
    data_file = os.path.join(os.path.dirname(__file__), '../../data/students.json')

    @classmethod
    def load_data(cls):
        if os.path.exists(cls.data_file):
            with open(cls.data_file, 'r') as f:
                return json.load(f)
        return []

    @classmethod
    def save_data(cls, data):
        with open(cls.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def add_student(cls, name, student_id):
        data = cls.load_data()
        student = {
            "id": student_id,
            "name": name,
            "progress": []
        }
        data.append(student)
        cls.save_data(data)
        print(f"Student added: {name}, ID: {student_id}")

    @classmethod
    def get_all_students(cls):
        return cls.load_data()

    @classmethod
    def get_student(cls, student_id):
        data = cls.load_data()
        for student in data:
            if student["id"] == student_id:
                return student
        return None

    @classmethod
    def add_progress(cls, student_id, quiz_name, total_score, test_score, time_taken):
        data = cls.load_data()
        for student in data:
            if student["id"] == student_id:
                student["progress"].append({
                    "quiz_name": quiz_name,
                    "total_score": total_score,
                    "test_score": test_score,
                    "time_taken": time_taken,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                cls.save_data(data)
                print(f"Progress added for student ID: {student_id}")
                return

    @classmethod
    def update_progress_with_default_time(cls):
        data = cls.load_data()
        for student in data:
            for progress in student["progress"]:
                if "time_taken" not in progress:
                    progress["time_taken"] = "N/A"
        cls.save_data(data)
