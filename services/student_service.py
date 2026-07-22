from models.student import Student
from dsa.hash_table import HashTable

class StudentService:
    def __init__(self):
        self.students_table = HashTable()
        self._load_students_from_json()

    def _load_students_from_json(self):
        """On startup, read students.json and build the hash table."""
        students = Student.load_students()
        for s in students:
            self.students_table.insertion(s["student_id"], s)

    def view_profile(self, student_id):
        """Look up a single student's profile by ID — O(1) via hash table."""
        student = self.students_table.get(student_id)

        if student is None:
            print(f"No student found with ID {student_id}.")
            return None

        print("=" * 35)
        print("Student Profile")
        print("=" * 35)
        print(f"ID:    {student['student_id']}")
        print(f"Name:  {student['name']}")
        print(f"Email: {student['email']}")
        print(f"Year:  {student['year']}")
        print(f"GPA:   {student['gpa']}")
        print("=" * 35)

        return student