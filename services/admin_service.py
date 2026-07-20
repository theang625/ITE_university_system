from models.admin import Admin
from models.course import Course
from models.student import Student
from dsa.hash_table import HashTable
from dsa.binary_tree import BinaryTree

from models.student import Student
from models.enrollment import Enrollment
import json
import os
 
class AdminService:
    
    def __init__(self):
        self.students_table = HashTable()
        self._load_table_from_json()

    def _load_table_from_json(self):
        """On startup, read students.json and rebuild the hash table."""
        students = Student.load_students()
        for s in students:
            self.students_table.insertion(s["student_id"], s)

    def add_student(self, student_id, name, email, year, gpa):
        # Fast duplicate check via hash table
        if self.students_table.get(student_id) is not None:
            print(f"Student ID {student_id} already exists.")
            return None

        new_student = {
            "student_id": student_id,
            "name": name,
            "email": email,
            "year": year,
            "gpa": gpa,
        }

        # Update hash table (memory)
        self.students_table.insertion(student_id, new_student)

        # Update JSON
        students = Student.load_students()
        students.append(new_student)
        Student.save_students(students)

        print(f"\tStudent '{name}' added successfully.")
        return new_student

    def delete_student(self, student_id):
        
        deleted = self.students_table.delete(student_id)
        
        if not deleted:
            print(f"Student ID {student_id} not found.")
            return False

        # Sync deletion to JSON
        students = Student.load_students()
        students = [s for s in students if s["student_id"] != student_id]
        Student.save_students(students)
        
        """Working on this please connect to the enrollment table"""
        # clean up this student's enrollment records too
        enrollments = Enrollment.load_enrollments()
        enrollments = [e for e in enrollments if e["student_id"] != student_id]
        Enrollment.save_enrollments(enrollments)
        
        print(f"Student ID {student_id} deleted.")
        return True

    def update_student(self, student_id, name=None, email=None, year=None, gpa=None):
        students = Student.load_students()

        student = None
        for s in students:
            if s["student_id"] == student_id:
                student = s
                break

        if student is None:
            print(f"Student ID {student_id} not found.")
            return None

        if email is not None:
            email_taken = any(
                s["email"] == email and s["student_id"] != student_id
                for s in students
            )
            if email_taken:
                print(f"Email '{email}' is already used by another student.")
                return None

        if name is not None:
            student["name"] = name
        if email is not None:
            student["email"] = email
        if year is not None:
            student["year"] = year
        if gpa is not None:
            student["gpa"] = gpa

        Student.save_students(students)

        print(f"Student ID {student_id} updated successfully.")
        return student

    def view_students(self):
        with open("students.json", "r") as f:
            students = json.load(f)
        
        for student in students:
            print(f"Student: id: {student['student_id']}, name: {student['name']}")

    def get_student(self, student_id):
        students = Student.load_students()
        for s in students:
            if s["student_id"] == student_id:
                return s
        return None

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
