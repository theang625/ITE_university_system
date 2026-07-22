import json
import os
from models.admin import Admin
from models.course import Course
from models.student import Student
from models.enrollment import Enrollment
from dsa.hash_table import HashTable
from dsa.binary_tree import BinaryTree

class AdminService:
    def __init__(self):
        # 1. Initialize Data Structures
        self.students_table = HashTable()
        self.courses_tree = BinaryTree()
  # Dedicated graph for course prerequisites

        # 2. Load Data into Memory on Startup
        self._load_table_from_json()
        self._load_courses_from_json()
        self._load_prereqs_from_json()

    def _load_table_from_json(self):
        """Rebuilds the student hash table from JSON on startup."""
        students = Student.load_students()
        for s in students:
            self.students_table.insertion(s["student_id"], s)

    def _load_courses_from_json(self):
        """Bonus: Rebuilds the course Binary Tree from JSON so it's not empty!"""
        file_path = "couse.json"  # Consider renaming this to courses.json later
        if not os.path.exists(file_path):
            return

        with open(file_path, "r") as f:
            courses = json.load(f)

        for c in courses:
            # Mapping JSON keys to your Course model
            course_obj = Course(c["course_id"], c["course_name"], credits=3)
            self.courses_tree.insert(c["course_id"], course_obj)
            self.enrollment_graph.add_vertex(c["course_id"])

    def _load_prereqs_from_json(self):
        """Loads course prerequisites into the prereq_graph."""
        file_path = "couser require.json"  # Consider renaming to course_requires.json
        if not os.path.exists(file_path):
            return

        with open(file_path, "r") as f:
            prereqs = json.load(f)

        for req in prereqs:
            course = req["course_id"]
            prerequisite = req["requires_course_id"]
            self.prereq_graph.add_edge(prerequisite, course)

    # ==========================================
    # STUDENT OPERATIONS
    # ==========================================
    def add_student(self, student_id, name, email, year, gpa):
        # Fast duplicate check via hash table (O(1) lookup!)
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

        # Update hash table (Memory)
        self.students_table.insertion(student_id, new_student)

        # Update JSON (Storage)
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

        # Clean up this student's enrollment records too
        enrollments = Enrollment.load_enrollments()
        enrollments = [e for e in enrollments if e["student_id"] != student_id]
        Enrollment.save_enrollments(enrollments)

        # Remove from enrollment graph
        self.enrollment_graph.remove_vertex(student_id)

        print(f"Student ID {student_id} deleted and enrollments cleared.")
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

        # Update fields
        if name is not None: student["name"] = name
        if email is not None: student["email"] = email
        if year is not None: student["year"] = year
        if gpa is not None: student["gpa"] = gpa

        # Save back to JSON
        Student.save_students(students)

        # Update Hash Table memory
        self.students_table.insertion(student_id, student)

        print(f"Student ID {student_id} updated successfully.")
        return student

    def view_students(self):
        with open("students.json", "r") as f:
            students = json.load(f)
        for student in students:
            print(f"Student ID: {student['student_id']}, Name: {student['name']}")

    def get_student(self, student_id):
        # We can now use the ultra-fast hash table instead of a slow loop!
        return self.students_table.get(student_id)

    # ==========================================
    # COURSE & ENROLLMENT OPERATIONS
    # ==========================================
    def add_course(self, course_id, course_code, course_name, year_level, active =  True):
        
        new_course = {
            "course_id": course_id,
            "course_code": course_code,
            "course_name": course_name,
            "year_level": year_level,
            "active": active
        }
        # self.courses_tree.insert(course_id, course)
        # self.enrollment_graph.add_vertex(course_id)
        # # Note: You should also append this to couse.json in the future
        # return course

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