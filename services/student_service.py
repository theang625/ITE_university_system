from models.student import Student
from dsa.hash_table import HashTable
from dsa.binary_tree import BinaryTree
from models.enrollment import Enrollment
from services.admin_service import AdminService
from datetime import datetime
from dsa.graph import Graph
class StudentService:
    def __init__(self, admin_service):
        self.students_table = HashTable()
        self._load_students_from_json()
        self.course_graph = Graph()
        
    admin_service = AdminService()        

    def _load_students_from_json(self):
        students = Student.load_students()
        for s in students:
            self.students_table.insertion(s["student_id"], s)

    def view_profile(self, student):
        
        if not student:
            print("\nError: Profile not found.\n")
            return

        student_id = student["student_id"]

        print("       MY PROFILE & COURSES".center(50))
        print(f"ID:    {student['student_id']}")
        print(f"Name:  {student['name']}")
        print(f"Email: {student['email']}")
        print(f"Year:  {student['year']}")
        print(f"GPA:   {student['gpa']}")
        print(" Enrolled Courses:")

        enrolled_course_ids = self.admin_service.enrollment_graph.get_neighbors(student_id)

        if not enrolled_course_ids:
            print("   [No courses registered yet]")
        else:
            for course_id in enrolled_course_ids:
                course = self.admin_service.get_course(course_id)
                if course:
                    print(f"   - ID: {course['course_id']} | {course['course_name']}")
                else:
                    print(f"   - ID: {course_id} (Details missing)")

        print("=" * 45)
        print()
        
    def view_rank_by_gpa(self, student_id=None):
        
        students = Student.load_students()

        if not students:
            print("No students found.")
            return

        gpa_tree = BinaryTree()
        for s in students:
            gpa = s["gpa"]
            existing = gpa_tree.search(gpa)
            if existing is not None:
                existing.append(s)        
            else:
                gpa_tree.insert(gpa, [s]) 

        sorted_by_gpa = gpa_tree.reverse_inorder()

        ranked_list = []
        rank = 1
        for gpa, student_group in sorted_by_gpa:
            for s in student_group:
                ranked_list.append((rank, s))
            rank += len(student_group) 

        print("=" * 50)
        print("STUDENT RANKING BY GPA".center(50))
        print("=" * 50)
        for r, s in ranked_list:
            print(f"  #{r:<3} {s['student_id']:<6} {s['name']:<20} GPA: {s['gpa']}")
        print("=" * 50)

        if student_id is not None:
            for r, s in ranked_list:
                if s["student_id"] == student_id:
                    print(f"\nYour rank: #{r} out of {len(ranked_list)} students (GPA: {s['gpa']})")
                    return r

            print(f"\nStudent ID {student_id} not found in ranking.")
            return None

        return ranked_list
    
    def enroll_self(self, student_id):

        student = self.admin_service.get_student_by_id(student_id)
        if not student:
            print("Error: Student profile not found.")
            return False

        current_course_ids = self.admin_service.enrollment_graph.get_neighbors(student_id)

        print(f"\nWelcome, {student['name']}!")
        print("Your current courses:")
        if not current_course_ids:
            print("   [No courses registered yet]")
        else:
            for c_id in current_course_ids:
                course = self.admin_service.courses_tree.search(c_id)
                if course:
                    print(f"   - ID: {course['course_id']} | {course['course_name']}")

        all_courses = [c for _, c in self.admin_service.courses_tree.inorder()]

        if not all_courses:
            print("No courses available right now.")
            return False

        print("\nAVAILABLE COURSES".center(50))
        print("-" * 50)
        for course in all_courses:
            tag = " (already enrolled)" if course["course_id"] in current_course_ids else ""
            print(f"   ID: {course['course_id']:<4} | {course['course_name']}{tag}")
        print("-" * 50)

        # 4. Ask for multiple course IDs at once
        courses_input = input("Enter Course IDs to enroll, separated by commas (e.g., 1, 3, 5): ")
        try:
            requested_ids = [int(c.strip()) for c in courses_input.split(",") if c.strip()]
        except ValueError:
            print("Invalid input. Please enter numeric course IDs separated by commas.")
            return False

        if not requested_ids:
            print("No course IDs entered.")
            return False

        # 5. Load enrollments once, before the loop (avoid repeated file reads)
        enrollments = Enrollment.load_enrollments()
        next_id = (max((e["enrollment_id"] for e in enrollments), default=0)) + 1

        enrolled_now = []
        skipped = []

        for course_id in requested_ids:
            # Skip if already enrolled
            if course_id in current_course_ids:
                skipped.append((course_id, "already enrolled"))
                continue

            # Skip if course doesn't exist
            course = self.admin_service.courses_tree.search(course_id)
            if not course:
                skipped.append((course_id, "course not found"))
                continue

            # Add edge in the graph (memory)
            self.admin_service.enrollment_graph.add_edge(student_id, course_id)

            # Build the new enrollment record
            new_enrollment = {
                "enrollment_id": next_id,
                "student_id": student_id,
                "course_id": course_id,
                "grade": None,
                "enrolled_date": datetime.now().strftime("%Y-%m-%d")
            }
            enrollments.append(new_enrollment)
            next_id += 1

            enrolled_now.append(course)
            current_course_ids.append(course_id)  # so duplicate checks within this same loop stay accurate

        # 6. Save once, after processing all requested courses
        Enrollment.save_enrollments(enrollments)

        # 7. Summary
        print("\n" + "=" * 50)
        if enrolled_now:
            print(f"Successfully enrolled in {len(enrolled_now)} course(s):")
            for c in enrolled_now:
                print(f"   - {c['course_id']}: {c['course_name']}")
        if skipped:
            print(f"\nSkipped {len(skipped)} course(s):")
            for c_id, reason in skipped:
                print(f"   - {c_id}: {reason}")
        print("=" * 50)

        return True
    