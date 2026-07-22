import json
import os
from utils.menu import *
from models.admin import Admin
from models.course import Course
from models.student import Student
from models.enrollment import Enrollment
from dsa.hash_table import HashTable
from dsa.binary_tree import BinaryTree
from dsa.graph import Graph
from dsa.stack import Stack

class AdminService:
    def __init__(self):
        # 1. Initialize Data Structures
        self.students_table = HashTable()
        self.courses_tree = BinaryTree()
        self.enrollment_graph = Graph()
        self.prereq_graph = Graph()  
        self.undo_stack = Stack()
        
        self._load_courses_from_json()
        self._load_table_from_json()
        self._load_courses_from_json()
        self._load_prereqs_from_json()
        self._load_enrollments_from_json() 
        self.courses_tree = BinaryTree()
        self.courses_tree.load_from_json("Course.json", "course_id")
        self.students_table = HashTable()
        self.students_table.load_from_json("students.json", "student_id")

    def _load_table_from_json(self):
        """Rebuilds the student hash table from JSON on startup."""
        students = Student.load_students()
        for s in students:
            self.students_table.insertion(s["student_id"], s)

    def _load_courses_from_json(self):
        """Rebuilds the course Binary Tree from JSON so it's not empty!"""
        file_path = "Course.json"
        if not os.path.exists(file_path):
            print(f"Warning: Course file not found at {file_path}")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            courses = json.load(f)

        for c in courses:
            c_id = c.get("course_code", c.get("course_id"))
            title = c.get("course_name", c.get("title", "Unknown Title"))
            credits = c.get("credits", 3)

            if c_id:
                course_obj = Course(c_id, title, credits)
                self.courses_tree.insert(c_id, course_obj)
                self.enrollment_graph.add_vertex(c_id)

    def _load_prereqs_from_json(self):
        """Loads course prerequisites into the prereq_graph."""
        file_path = "course_require.json"  # Clean filename convention
        if not os.path.exists(file_path):
            return

        with open(file_path, "r", encoding="utf-8") as f:
            prereqs = json.load(f)

        for req in prereqs:
            course = req.get("course_id")
            prerequisite = req.get("requires_course_id")
            if course and prerequisite:
                self.prereq_graph.add_edge(prerequisite, course)

    def _load_enrollments_from_json(self):
        """Loads enrollments from Enrollment.json into the graph on startup."""
        file_path = "Enrollment.json"
        if not os.path.exists(file_path):
            return

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for item in data:
                    s_id = item.get("student_id")
                    c_id = item.get("course_id")
                    if s_id and c_id:
                        self.enrollment_graph.add_edge(s_id, c_id)
            except Exception as e:
                print(f"Error loading enrollments: {e}")

    def save_enrollments_to_json(self):
        """Saves current graph enrollments to Enrollment.json safely without crashing."""
        file_path = "Enrollment.json"
        all_enrollments = []

        try:
            vertices = []
            if hasattr(self.enrollment_graph, 'get_vertices') and callable(self.enrollment_graph.get_vertices):
                vertices = self.enrollment_graph.get_vertices()
            elif hasattr(self.enrollment_graph, 'vertices'):
                v_attr = self.enrollment_graph.vertices
                vertices = v_attr.keys() if callable(getattr(v_attr, 'keys', None)) else v_attr
            elif hasattr(self.enrollment_graph, 'adjacency_list'):
                adj = self.enrollment_graph.adjacency_list
                vertices = adj.keys() if not callable(adj) else adj().keys()

            for student_id in vertices:
                courses = self.enrollment_graph.get_neighbors(student_id)
                for c_id in courses:
                    all_enrollments.append({
                        "student_id": student_id,
                        "course_id": c_id
                    })
        except Exception as e:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    all_enrollments = json.load(f)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(all_enrollments, f, indent=4)

    # ==========================================
    # STUDENT OPERATIONS
    # ==========================================
    
    def generate_student_id(self):
        """Auto-generate the next student_id in S01, S02... format."""
        students = Student.load_students()

        if not students:
            return "S01"

        # Extract the numeric part from each ID (e.g. "S12" -> 12)
        numbers = [int(student["student_id"][1:]) for student in students]
        next_number = max(numbers) + 1

        return f"S{next_number}"  # pads with a leading zero if needed (S01–S09), grows naturally past S99
    def add_student(self, student_id, name, email, year, gpa):
        
        student_id = self.generate_student_id()
        
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

        self.students_table.insertion(student_id, new_student)

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

        students = Student.load_students()
        students = [s for s in students if s["student_id"] != student_id]
        Student.save_students(students)

        enrollments = Enrollment.load_enrollments()
        enrollments = [e for e in enrollments if e["student_id"] != student_id]
        Enrollment.save_enrollments(enrollments)

        self.enrollment_graph.remove_vertex(student_id)
        self.save_enrollments_to_json()  # Save graph changes

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

        if name is not None: student["name"] = name
        if email is not None: student["email"] = email
        if year is not None: student["year"] = year
        if gpa is not None: student["gpa"] = gpa

        Student.save_students(students)
        self.students_table.insertion(student_id, student)
        print(f"Student ID {student_id} updated successfully.")
        return student

    def view_students(self):
        """Load students into the hash table, then display via the hash table."""
        
        # 1. Load from JSON and insert into hash table (one by one)
        students = Student.load_students()
        for student in students:
            self.students_table.insertion(student["student_id"], student)

        # 2. Display by reading from the hash table, not directly from JSON
        all_students = self.students_table.values()

        if not all_students:
            print("No students found.")
            return []

        print("-" * 60)
        print("STUDENT LIST".center(60))
        print("-" * 60)
        for student in all_students:
            print(f"ID: {student['student_id']:<6} "
                f"Name: {student['name']:<20} "
                f"Email: {student['email']:<30} "
                f"Year: {student['year']:<3} "
                f"GPA: {student['gpa']}")
        print("=" * 60)

        return

    def get_student_by_id(self, student_id):
        """Alias for get_student for consistency."""
        return self.students_table.get(student_id)
    
    def search_students_by_name(self, name_query):
        """Searches for students whose names contain the given query string (case-insensitive)."""
        file_path = "students.json"
        matching_students = []

        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    students_data = json.load(f)
                    for s in students_data:
                        if name_query.lower() in s.get("name", "").lower():
                            matching_students.append(s)
            except Exception as e:
                print(f"Error reading students file: {e}")

        return matching_students

    # ==========================================
    # COURSE & ENROLLMENT OPERATIONS
    # ==========================================
    def add_course(self, course_id, course_code, course_name, year_level, active=True):
    # Check for duplicates first
        if self.courses_tree.search(course_id) is not None:
            print(f"Course ID {course_id} already exists.")
            return None
        active = True
        new_course = {
            "course_id": course_id,
            "course_code": course_code,
            "course_name": course_name,
            "year_level": year_level,
            "active": active
        }
        self.courses_tree.insert(course_id, new_course)
        self.enrollment_graph.add_vertex(course_id)

        courses = Course.load_courses()
        courses.append(new_course)
        Course.save_courses(courses)

        print(f"Course '{course_name}' added successfully.")
        return new_course

    def delete_course(self, course_id):
        print(f"Trying to delete: {repr(course_id)}")  # debug line

        removed = self.courses_tree.remove(course_id)
        print(f"Tree said removed = {removed}")  # debug line

        if not removed:
            print(f"Course ID {course_id} not found.")
            return False

        courses = Course.load_courses()
        print(f"Courses before: {courses}")  # debug line

        courses = [c for c in courses if c["course_id"] != course_id]
        print(f"Courses after: {courses}")  # debug line

        Course.save_courses(courses)

        if removed:
            print(f"Course ID {course_id} deleted successfully.")
        return True

    def view_courses(self):
        """Step 3: Traverse the tree (in-order = sorted by course_id) and display."""
        courses = [course for _, course in self.courses_tree.inorder()]

        if not courses:
            print("No courses found.")
            return []

        print("=" * 60)
        print("COURSE LIST (sorted by ID via tree traversal)".center(60))
        print("=" * 60)
        for course in courses:
            print(f"ID: {course['course_id']:<5} "
                  f"Code: {course['course_code']:<10} "
                  f"Name: {course['course_name']:<20} "
                  f"Year: {course['year_level']:<3} "
                  f"Active: {course['active']}")
        print("=" * 60)

        return 

    def get_course(self, course_id):
        """Safely searches for a course in the binary tree by handling type matching."""
        result = self.courses_tree.search(course_id)
        if result:
            return result

        try:
            if isinstance(course_id, str):
                alt_id = int(course_id)
            else:
                alt_id = str(course_id)
            return self.courses_tree.search(alt_id)
        except (ValueError, TypeError):
            return None

    def check_prerequisites(self, student_id, course_id):
        """Checks if a student has completed the prerequisites for a course."""
        required_courses = self.prereq_graph.get_neighbors(course_id)
        if not required_courses:
            return True 

        enrolled_courses = self.enrollment_graph.get_neighbors(student_id)

        for req in required_courses:
            if req not in enrolled_courses:
                print(
                    f"⚠️ Prerequisite Error: Course {course_id} requires prerequisite [{req}], which the student has not completed yet.")
                return False
        return True

    def enroll_student(self, student_id, course_id):

        if not self.check_prerequisites(student_id, course_id):
            return False

        self.enrollment_graph.add_edge(student_id, course_id)
        self.save_enrollments_to_json() 
        return True

    # ==========================================
    # UNDO STACK LOGIC
    # ==========================================
    def admin_drop_course(self, student_id, course_id):
        """Admin removes a course, but we save it in case of a mistake."""
        if self.enrollment_graph.remove_edge(student_id, course_id):
            action_log = {
                "type": "drop_course",
                "student_id": student_id,
                "course_id": course_id
            }

            self.undo_stack.push(action_log)
            self.save_enrollments_to_json() 
            print(f"Success: Dropped {course_id} for {student_id}.")
            return True

        print("Error: Could not drop course.")
        return False