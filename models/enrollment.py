import json
import os

_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "Enrollment.json")
_JSON_PATH = os.path.abspath(_JSON_PATH)

class Enrollment:
    def __init__(self, enrollment_id, student_id, course_id, grade, enrolled_date):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade
        self.enrolled_date = enrolled_date

    @staticmethod
    def load_enrollments():
        if not os.path.exists(_JSON_PATH):
            return []
        with open(_JSON_PATH, "r") as f:
            return json.load(f)

    @staticmethod
    def save_enrollments(enrollments):
        with open(_JSON_PATH, "w") as f:
            json.dump(enrollments, f, indent=4)