import json
import os
class Course:
    def __init__(self, course_id, course_code, course_name, year_level, active =  True):
        self.course_id = course_id
        self.course_code = course_code
        self.course_name = course_name
        self.year_level = year_level
        self.active = active
    
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
