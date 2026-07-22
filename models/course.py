import json
import os
class Course:
    def __init__(self, course_id, title, credits):
        self.course_id = course_id
        self.title = title
        self.credits = credits
    
    @staticmethod
    def load_courses():
        if not os.path.exists("Course.json"):
            return []
        with open("Course.json", "r") as f:
            return json.load(f)

    @staticmethod
    def save_courses(courses):
        with open("Course.json", "w") as f:
            json.dump(courses, f, indent=4)
