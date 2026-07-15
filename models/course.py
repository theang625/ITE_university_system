class Course:
    def __init__(self, course_id, title, credits):
        self.course_id = course_id
        self.title = title
        self.credits = credits

    def __repr__(self):
        return f"Course({self.course_id}, {self.title}, {self.credits})"
