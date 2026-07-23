from services.admin_service import AdminService
from services.student_service import StudentService
from models.student import Student
from dsa.hash_table import HashTable
from models.admin import Admin
from models.course import Course
import json

admin_service = AdminService()
student_service = StudentService(admin_service)

def show_main_menu():
    print("MAIN MENU".center(45))
    print("=" * 45)
    print("  1. Admin Login")
    print("  2. Student Login")
    print("  3. Exit")
    print("=" * 45)


def login(username, password):
    admins = Admin.load_admins()

    for i in range(len(admins)):
        if admins[i]["username"] == username and admins[i]["password"] == password:
            print(f"Login successful. Welcome, {admins[i]['username']} (admin ID {i})")
            show_admin_menu()
            return True

    print("Invalid username or password")
    return False

def student_login(username, password):
    try:
        with open("Userstudent.json", "r") as f:
            users = json.load(f)

        for user in users:
            if user.get("username") == username and user.get("password") == password:
                print(f"\nLogin successful! Welcome, {username}.")
                linked_id = user.get("linked_student_id")
                show_student_menu(linked_id)
                return True

        print("\nInvalid username or password. Please try again.")
        return False

    except FileNotFoundError:
        print(f"Error: Could not find 'Userstudent.json'. Please check the file name.")
        return False

def generate_course_id() :
    courses = Course.load_courses()
    
    if not courses:
        return 1

    numbers = [(course["course_id"]) for course in courses]
    next_number = max(numbers) + 1

    return next_number
    
def show_admin_menu():
    while True:
        print("=" * 35)
        print(" " * 4, end=" ")
        print("Welcome to Admin Menu")
        print("=" * 30)
        print("\nAdmin Menu")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Update Student")
        print("4. View Students")
        print("5. Enter student Name to search") 
        print("6. Add Course")
        print("7. Delete Course")
        print("8. Undo Last Action")
        print("9. Enroll Student in Multiple Courses")
        print("10. Drop Course for Student (Un-enroll)")
        print("11. View all Courses.")
        print("0. Logout")

        choice = input("Enter your choice for admin menu: ")

        if choice == "1":
            name = str(input("Enter student name: "))
            email = str(input("Enter student email: "))
            year = int(input("Enter student year: "))
            gpa = float(input("Enter student GPA: "))

            student_id = admin_service.generate_student_id() 
            result = admin_service.add_student(student_id, name, email, year, gpa)

            if result is not None:
                print(f"Student added successfully with ID: {student_id}")

        elif choice == "2":
            student_id = str(input("Enter student ID to delete: "))
            deleted = admin_service.delete_student(student_id)
            if deleted:
                print("Student deleted successfully")

        elif choice == "3":
            student_id = str(input("Enter student ID to update: "))
            name = input("Enter new name (leave blank to keep): ")
            email = input("Enter new email (leave blank to keep): ")
            year_input = input("Enter new year (leave blank to keep): ")
            gpa_input = input("Enter new GPA (leave blank to keep): ")

            year = int(year_input) if year_input else None
            gpa = float(gpa_input) if gpa_input else None

            result = admin_service.update_student(student_id, name or None, email or None, year, gpa)
            if result is not None:
                print("Student updated successfully")

        elif choice == "4":
            print(admin_service.view_students())

        elif choice == "5":
            print("\n" + "=" * 40)
            print("       SEARCH STUDENT BY NAME")
            print("=" * 40)
            name_query = input("Enter student name : ").strip()

            if not name_query:
                print("Please enter a valid name to search.")
            else:
                results = admin_service.search_students_by_name(name_query)
                if not results:
                    print(f" No students found matching '{name_query}'.")
                else:
                    print(f"\nFound {len(results)} student(s):")
                    print("=" * 45)
                    for s in results:
                        print(f"ID:    {s.get('student_id', s.get('id'))}")
                        print(f"Name:  {s.get('name')}")
                        print(f"Email: {s.get('email')}")
                        print(f"Year:  {s.get('year')}")
                        print(f"GPA:   {s.get('gpa')}")
                        print("-" * 45)
            print("=" * 40 + "\n")

        elif choice == "6":
            course_code = input("Enter course code: ")
            course_name = input("Enter course name: ")
            year_level = int(input("Enter year level: "))
            active = bool(input("Keep it blank for active course: "))
            
            course_id = generate_course_id()
            
            result = admin_service.add_course(course_id, course_code, course_name, year_level, active)
            if result:
                print("Course added successfully")

        elif choice == "7":
            course_id = int(input("Enter course ID to delete: "))
            admin_service.delete_course(course_id)
            print("Course deleted successfully")

        elif choice == "8":
            print("\n" + "=" * 35)
            print("          UNDO SYSTEM")
            print("=" * 35)

            last_action = admin_service.undo_stack.pop()

            if not last_action:
                print("History is empty. Nothing to undo!")
            else:
                if last_action["type"] == "drop_course":
                    s_id = last_action["student_id"]
                    c_id = last_action["course_id"]

                    admin_service.enrollment_graph.add_edge(s_id, c_id)
                    print(f" UNDO SUCCESS: Re-enrolled Student ID {s_id} back into Course {c_id}.")

            print("=" * 35 + "\n")

        elif choice == "9":
            print("\n--- Enroll Student in Multiple Courses ---")
            try:
                student_id = str(input("Enter Student ID: "))

                current_courses = admin_service.enrollment_graph.get_neighbors(student_id)

                if current_courses:
                    print(f"\nStudent {student_id} is currently enrolled in {len(current_courses)} course(s):")
                    for c_id in current_courses:
                        course = admin_service.courses_tree.search(c_id)
                        if course:
                            print(f"  ID: {course['course_id']:<4} | {course['course_name']}")
                        else:
                            print(f"  ID: {c_id} | (course details not found)")
                else:
                    print(f"\nStudent {student_id} is not currently enrolled in any courses.")

                all_courses = [course for _, course in admin_service.courses_tree.inorder()]

                if not all_courses:
                    print("No courses available to enroll in.")
                else:
                    print("\n" + "AVAILABLE COURSES".center(50))
                    print("=" * 50)
                    for course in all_courses:
                        print(f"  ID: {course['course_id']:<4} | {course['course_name']}")
                    print("=" * 50)

                    courses_input = input("\nEnter Course IDs separated by commas (e.g., 1, 3, 7): ")
                    course_ids = [int(c.strip()) for c in courses_input.split(",") if c.strip()]  # <-- fixed

                    if not course_ids:
                        print("No valid course IDs provided.")
                    else:
                        success_count = 0
                        for c_id in course_ids:
                            if admin_service.enroll_student(student_id, c_id):
                                success_count += 1
                        print(
                            f"SUCCESS: Enrolled Student ID {student_id} into {success_count} course(s): {', '.join(str(c) for c in course_ids)}")
            except ValueError:
                print("Invalid input. Student ID must be a number or contains a non-numeric course ID.")
                
        elif choice == "10": 
            student_id = input("Enter student ID: ")  
            admin_service.admin_drop_course(student_id)  
            
        elif choice == "11":
            print("View Courses: ")
            print(admin_service.view_courses())
                
        elif choice == "0":
            print("Logged out")
            break
        else:
            print("Invalid choice")
            
def show_student_menu(student_id):
    while True:
        print("\n" + "=" * 40)
        print("Welcome to Student Menu")
        print("=" * 40)
        print("1. View Profile & My Courses.")
        print("2. View aveliable courses.")
        print("3. View my GPA rank.")
        print("4. Enroll into a course.")
        print("5. Go back to Main Menu.")

        choice = input("Enter your choice for student menu: ")

        if choice == "1":
            student = admin_service.get_student_by_id(student_id)  # matches actual method name
            student_service.view_profile(student)
        
        elif choice == "2":
            print("Available Courses: ")
            print(admin_service.view_courses())
        
        elif choice == "3":
            print("View my GPA rank.")
            student = admin_service.get_student_by_id(student_id)
            student_service.view_rank_by_gpa(student_id)
            
        elif choice == "4":
            print("Enroll into a course.")
            student = admin_service.get_student_by_id(student_id)
            student_service.enroll_self(student_id)

        elif choice == "5":
            print("Going back to Main Menu...")
            break

        else:
            print("Invalid choice. Try again.")


def get_student():
    print("Student List.")
    print("=" * 35)
    with open("students.json", "r") as f:
        students_data = json.load(f)
    for student in students_data:
        print(f"Student: id: {student['id']}, name: {student['name']}")