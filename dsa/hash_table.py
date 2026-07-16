import json
import math
import os
from services import admin_service

class HashTable:
    def __init__(self, size=50):
        self.size = size
        self.table = [[] for _ in range(size)]

    # ----------------------------
    # Hash Function
    # ----------------------------
    def _hash(self, key):
        A = 0.6180339887
        return math.floor(self.size * ((int(key) * A) % 1))

    # ----------------------------
    # Insert Student
    # ----------------------------
    def insert(self, student):
        
        key = student["id"]
        index = self._hash(key)

        # Update if already exists
        for item in self.table[index]:
            if item["id"] == key:
                item.update(student)
                return

        self.table[index].append(student)

    # ----------------------------
    # Search Student
    # ----------------------------
    def get(self, key):
        index = self._hash(key)

        for item in self.table[index]:
            if item["id"] == key:
                return item

        return None

    # ----------------------------
    # Delete Student
    # ----------------------------
    def delete(self, key):
        index = self._hash(key)

        for item in self.table[index]:
            if item["id"] == key:
                self.table[index].remove(item)
                return True

        return False

    # ----------------------------
    # Update Student
    # ----------------------------
    def update(self, key, **kwargs):
        student = self.get(key)

        if student:
            student.update(kwargs)
            return True

        return False

    # ----------------------------
    # Return all students
    # ----------------------------
    def values(self):
        students = []

        for bucket in self.table:
            students.extend(bucket)

        return students

    # ----------------------------
    # Load JSON File
    # ----------------------------
    def load_json(self, filename):
        if not os.path.exists(filename):
            return

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for student in data:
            self.insert(student)

    # ----------------------------
    # Save JSON File
    # ----------------------------
    def save_json(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.values(), file, indent=4)