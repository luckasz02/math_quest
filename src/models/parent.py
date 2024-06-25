import json
import os

class Parent:
    data_file = os.path.join(os.path.dirname(__file__), '../../data/parents.json')

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
    def add_parent(cls, name, parent_id, children_ids):
        data = cls.load_data()
        parent = {
            "id": parent_id,
            "name": name,
            "children_ids": children_ids
        }
        data.append(parent)
        cls.save_data(data)
        print(f"Parent added: {name}, ID: {parent_id}")

    @classmethod
    def get_all_parents(cls):
        return cls.load_data()

    @classmethod
    def get_parent(cls, parent_id):
        data = cls.load_data()
        for parent in data:
            if parent["id"] == parent_id:
                return parent
        return None
