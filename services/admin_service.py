from models.admin import Admin
from models.course import Course
from models.student import Student
from dsa.hash_table import HashTable
from dsa.binary_tree import BinaryTree
from dsa.graph import Graph
import json
 

class AdminService:
    def __init__(self):
        self.admins = []
        self.admins_table = HashTable()
        self.courses_tree = BinaryTree()
        self.enrollment_graph = Graph()

    def add_admin(self, admin_id, name):
        admin = Admin(admin_id, name)
        
        self.admins_table.insertion(admin_id, name)
        return admin

    def add_student(self, student_id, name, email, gpa):
        student = Student(student_id, name, email, gpa)
        HashTable.student_insert(student_id, name, email, gpa)
        self.enrollment_graph.add_vertex(student_id)
        return student

    def delete_student(self, student_id):
        deleted = self.students_table.delete(student_id)
        if deleted:
            self.enrollment_graph.remove_vertex(student_id)
        return deleted

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
