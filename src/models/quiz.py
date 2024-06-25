import json
import os
import random

class Quiz:
    data_file = os.path.join(os.path.dirname(__file__), '../../data/quizzes.json')

    @classmethod
    def load_data(cls):
        if os.path.exists(cls.data_file):
            with open(cls.data_file, 'r') as f:
                return json.load(f)
        return {}

    @classmethod
    def save_data(cls, data):
        with open(cls.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def create_quiz(cls, quiz_name):
        data = cls.load_data()
        if quiz_name not in data:
            data[quiz_name] = {"levels": {}}
        cls.save_data(data)
        print(f"Created quiz: {quiz_name}")

    @classmethod
    def add_question(cls, quiz_name, level, question, answer, hint):
        data = cls.load_data()
        if quiz_name not in data:
            data[quiz_name] = {"levels": {}}
        if str(level).lower() != "test":
            if str(level) not in data[quiz_name]["levels"]:
                data[quiz_name]["levels"][str(level)] = []
            data[quiz_name]["levels"][str(level)].append({"question": question, "answer": answer, "hint": hint})
        cls.save_data(data)
        print(f"Added question to quiz: {quiz_name}, level: {level}")

    @classmethod
    def create_test_level(cls, quiz_name):
        data = cls.load_data()
        if quiz_name in data:
            levels = data[quiz_name]["levels"].keys()
            test_questions = []
            for level in levels:
                if level.lower() != "test":
                    test_questions.extend(data[quiz_name]["levels"][level])
            random.shuffle(test_questions)
            data[quiz_name]["levels"]["Test"] = test_questions[:10]
            cls.save_data(data)
            print(f"Test level created for quiz: {quiz_name}")

    @classmethod
    def get_all_quizzes(cls):
        data = cls.load_data()
        print(f"Loaded quizzes: {data}")
        return data

    @classmethod
    def exists(cls, quiz_name):
        data = cls.load_data()
        return quiz_name in data

    @classmethod
    def get_questions(cls, quiz_name, level):
        data = cls.load_data()
        return data.get(quiz_name, {}).get("levels", {}).get(str(level), [])

    @classmethod
    def get_levels(cls, quiz_name):
        data = cls.load_data()
        return data.get(quiz_name, {}).get("levels", {}).keys()