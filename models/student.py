import json
import os

class Student:
    def __init__(self, student_id, name, email, year, gpa):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.year = year
        self.gpa = gpa

    @staticmethod
    def load_students():
        if not os.path.exists("students.json"):
            return []
        with open("students.json", "r") as f:
            return json.load(f)

    @staticmethod
    def save_students(students):
        with open("students.json", "w") as f:
            json.dump(students, f, indent=4)
            
    @staticmethod
    def load_users():
        if not os.path.exists("Userstudent.json"):
            return []
        with open("Userstudent.json", "r") as f:
            return json.load(f)