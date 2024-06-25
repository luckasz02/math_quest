import json
import os

class Teacher:
    data_file = os.path.join(os.path.dirname(__file__), '../../data/teachers.json')

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
    def exists(cls, username):
        data = cls.load_data()
        return username in data

    @classmethod
    def create(cls, username, password):
        data = cls.load_data()
        data[username] = password
        cls.save_data(data)

    @classmethod
    def authenticate(cls, username, password):
        data = cls.load_data()
        return data.get(username) == password
