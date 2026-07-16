from models.admin import Admin
from models.course import Course
from models.student import Student
from dsa.hash_table import HashTable
from dsa.binary_tree import BinaryTree
from dsa.graph import Graph
from models.student import Student
from models.enrollment import Enrollment
import json
import os
 
class AdminService:
    def __init__(self):
        self.admins = []
        self.hash_table = HashTable()
        self.courses_tree = BinaryTree()
        self.enrollment_graph = Graph()

    def add_admin(self, admin_id, name):
        admin = Admin(admin_id, name)
        
        self.admins_table.insertion(admin_id, name)
        return admin

    def add_student(self, student_id, name, email, year, gpa):
        students = Student.load_students()  # no instance needed

        new_student = {
            "student_id": student_id,
            "name": name,
            "email": email,
            "year": year,
            "gpa": gpa,
        }
        
        if any(s["student_id"] == student_id for s in students):
            print(f"Student ID {student_id} already exists. With name: {name}")
            return None
        else:
            students.append(new_student)
            Student.save_students(students)
            print(f"Student '{name}' added successfully.") 
        
        return new_student

    def delete_student(self, student_id):
        students = Student.load_students()

        student_exists = any(s["student_id"] == student_id for s in students)
        if not student_exists:
            print(f"Student ID {student_id} not found.")
            return False

        students = [s for s in students if s["student_id"] != student_id]
        Student.save_students(students)

        # clean up this student's enrollment records too
        enrollments = Enrollment.load_enrollments()
        enrollments = [e for e in enrollments if e["student_id"] != student_id]
        Enrollment.save_enrollments(enrollments)

        print(f"Student ID {student_id} deleted successfully.")
        return True

    def update_student(self, student_id, name=None, email=None):
        student = self.students_table.get(student_id)
        if student is None:
            return None
        if name is not None:
            student.name = name
        if email is not None:
            student.email = email
        return student

    def view_students(self):
        return self.students_table.values()

    def get_student(self, student_id):
        return self.students_table.get(student_id)

    def add_course(self, course_id, title, credits):
        course = Course(course_id, title, credits)
        self.courses_tree.insert(course_id, course)
        self.enrollment_graph.add_vertex(course_id)
        return course

    def delete_course(self, course_id):
        self.courses_tree.remove(course_id)
        self.enrollment_graph.remove_vertex(course_id)
        return True

    def view_courses(self):
        return [course for _, course in self.courses_tree.inorder()]

    def get_course(self, course_id):
        return self.courses_tree.search(course_id)

    def enroll_student(self, student_id, course_id):
        self.enrollment_graph.add_edge(student_id, course_id)
        return True
