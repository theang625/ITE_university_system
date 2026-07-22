import json
import os
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
        self.prereq_graph = Graph()  # Dedicated graph for course prerequisites

        # 🚀 NEW: Initialize the Undo Stack
        self.undo_stack = Stack()

        # 2. Load Data into Memory on Startup
        self._load_table_from_json()
        self._load_courses_from_json()
        self._load_prereqs_from_json()
        self._load_enrollments_from_json()  # 🔄 Load graph enrollments on startup

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
            # គាំទ្រទាំង course_code និង course_id ពីក្នុង JSON
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

    # 🔄 មុខងារទាញយកទិន្នន័យ Enrollment ពេលបើកកម្មវិធី (Graph Persistence Load)
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
            # ឆែកមើល Method ផ្សេងៗដែល Graph អាចមានដើម្បីទយក Vertices
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
            # គ្នារឿងភ័យព្រួយ ប្រសិនបើកន្លែងនេះទាញមិនចេញ គឺយើងអាន File ចាស់មកទុកសិនដើម្បីកុំឱ្យបាត់ទិន្នន័យ
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    all_enrollments = json.load(f)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(all_enrollments, f, indent=4)

    # ==========================================
    # STUDENT OPERATIONS
    # ==========================================
    def add_student(self, student_id, name, email, year, gpa):
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
        with open("students.json", "r", encoding="utf-8") as f:
            students = json.load(f)
        for student in students:
            print(f"Student ID: {student['student_id']}, Name: {student['name']}")

    def get_student(self, student_id):
        return self.students_table.get(student_id)

    def get_student_by_id(self, student_id):
        """Alias for get_student for consistency."""
        return self.students_table.get(student_id)

    # 🚀 មុខងារស្វែងរកសិស្សតាមឈ្មោះ (Search by Name)
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
    def add_course(self, course_id, title, credits):
        course = Course(course_id, title, credits)
        self.courses_tree.insert(course_id, course)
        self.enrollment_graph.add_vertex(course_id)
        return course

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
        """Returns all courses by traversing the binary tree in-order."""
        self._load_courses_from_json()
        return [course for _, course in self.courses_tree.inorder()]

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

    # 🛡️ មុខងារឆែកមុខវិជ្ជាត្រួតពិនិត្យមុន (Prerequisite Validation)
    def check_prerequisites(self, student_id, course_id):
        """Checks if a student has completed the prerequisites for a course."""
        required_courses = self.prereq_graph.get_neighbors(course_id)
        if not required_courses:
            return True  # អត់មានទាមទារមុខវិជ្ជាមុនទេ

        enrolled_courses = self.enrollment_graph.get_neighbors(student_id)

        for req in required_courses:
            if req not in enrolled_courses:
                print(
                    f"⚠️ Prerequisite Error: Course {course_id} requires prerequisite [{req}], which the student has not completed yet.")
                return False
        return True

    def enroll_student(self, student_id, course_id):
        # ឆែក Prerequisites មុននឹងអនុញ្ញាតឱ្យ Enroll
        if not self.check_prerequisites(student_id, course_id):
            return False

        self.enrollment_graph.add_edge(student_id, course_id)
        self.save_enrollments_to_json()  # 💾 Save ចូល file ស្វ័យប្រវត្តិ
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
            self.save_enrollments_to_json()  # 💾 Save ចូល file ស្វ័យប្រវត្តិក្រោយពេល Drop
            print(f"Success: Dropped {course_id} for {student_id}.")
            return True

        print("Error: Could not drop course.")
        return False