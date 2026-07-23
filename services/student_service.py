from models.student import Student
from dsa.hash_table import HashTable
from dsa.binary_tree import BinaryTree
class StudentService:
    def __init__(self, admin_service):
        self.students_table = HashTable()
        self._load_students_from_json()
        self.admin_service = admin_service  # shared reference to graph/tree

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
        """
        Loads all students' GPA into a tree, sorts them high-to-low via
        reverse in-order traversal, and displays the ranking.
        If student_id is given, also reports that student's specific rank.
        """
        # 1. Load students from JSON
        students = Student.load_students()

        if not students:
            print("No students found.")
            return

        # 2. Build a GPA tree — key = gpa, value = list of students with that GPA
        gpa_tree = BinaryTree()
        for s in students:
            gpa = s["gpa"]
            existing = gpa_tree.search(gpa)
            if existing is not None:
                existing.append(s)          # another student shares this GPA
            else:
                gpa_tree.insert(gpa, [s])   # new GPA, start a new list

        # 3. Reverse in-order traversal = GPA sorted highest to lowest
        sorted_by_gpa = gpa_tree.reverse_inorder()

        # 4. Flatten into a ranked list, assigning rank numbers
        ranked_list = []
        rank = 1
        for gpa, student_group in sorted_by_gpa:
            for s in student_group:
                ranked_list.append((rank, s))
            rank += len(student_group)   # students sharing a GPA share... actually next rank continues after the group

        # 5. Display the full leaderboard
        print("=" * 50)
        print("STUDENT RANKING BY GPA".center(50))
        print("=" * 50)
        for r, s in ranked_list:
            print(f"  #{r:<3} {s['student_id']:<6} {s['name']:<20} GPA: {s['gpa']}")
        print("=" * 50)

        # 6. If a specific student_id was given, report their rank directly
        if student_id is not None:
            for r, s in ranked_list:
                if s["student_id"] == student_id:
                    print(f"\nYour rank: #{r} out of {len(ranked_list)} students (GPA: {s['gpa']})")
                    return r

            print(f"\nStudent ID {student_id} not found in ranking.")
            return None

        return ranked_list