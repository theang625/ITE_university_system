from models.student import Student

class StudentService:
    def __init__(self):
        self.students = []

    def add_student(self, student_id, name, email):
        student = Student(student_id, name, email)
        self.students.append(student)
        return student

    def delete_student(self, student_id):
        self.students = [student for student in self.students if student.student_id != student_id]
        return True

    def update_student(self, student_id, name=None, email=None):
        for student in self.students:
            if student.student_id == student_id:
                if name is not None:
                    student.name = name
                if email is not None:
                    student.email = email
                return student
        return None

    def view_students(self):
        return self.students
