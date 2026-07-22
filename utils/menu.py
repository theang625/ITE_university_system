from services.admin_service import AdminService
from models.student import Student
from dsa.hash_table import HashTable
from models.admin import Admin
import json

admin_service = AdminService()

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


def get_admins():
    with open("admins.json", "r") as f:
        admins_data = json.load(f)

    for admin in admins_data:
        print(f"Username: {admin['username']}")
    return show_main_menu()


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
        print("5. Enter student ID to search")
        print("6. Add Course")
        print("7. Delete Course")
        print("8. Logout")
        print("9. Undo Last Action")
        print("10. Drop Course for Student (Un-enroll)")
        print("11. Enroll Student in Multiple Courses ")  # ធ្វើបច្ចុប្បន្នភាពមុខងារថ្មី

        choice = input("Enter your choice for admin menu: ")

        if choice == "1":
            student_id = int(input("Enter student ID: "))
            name = str(input("Enter student name: "))
            email = str(input("Enter student email: "))
            year = int(input("Enter student year: "))
            gpa = float(input("Enter student GPA: "))

            result = admin_service.add_student(student_id, name, email, year, gpa)
            if result is not None:
                print("Student added successfully")

        elif choice == "2":
            student_id = int(input("Enter student ID to delete: "))
            deleted = admin_service.delete_student(student_id)
            if deleted:
                print("Student deleted successfully")

        elif choice == "3":
            student_id = int(input("Enter student ID to update: "))
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
            student_id = int(input("Enter student ID or Name to search: "))
            student = admin_service.get_student_by_id(student_id)
            if student:
                print("=" * 35)
                print(f"ID: {student['student_id']}")
                print(f"Name: {student['name']}")
                print(f"Email: {student['email']}")
                print(f"Year: {student['year']}")
                print(f"GPA: {student['gpa']}")
            else:
                print(f"Student ID {student_id} not found.")

        elif choice == "6":
            course_id = input("Enter course ID: ")
            title = input("Enter course title: ")
            credits = int(input("Enter credits: "))
            admin_service.add_course(course_id, title, credits)
            print("Course added successfully")

        elif choice == "7":
            course_id = input("Enter course ID to delete: ")
            admin_service.delete_course(course_id)
            print("Course deleted successfully")

        elif choice == "8":
            print("Logged out")
            break

        elif choice == "9":
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

        elif choice == "10":
            print("\n--- Un-enroll Student ---")
            student_id = int(input("Enter Student ID: "))
            course_id = input("Enter Course ID to drop: ")

            admin_service.admin_drop_course(student_id, course_id)

        # 🚀 មុខងារថ្មី៖ Admin អាច Enroll មុខវិជ្ជាច្រើនព្រមគ្នាដោយខ័ណ្ឌដោយសញ្ញាក្បៀស (,)
        elif choice == "11":
            print("\n--- Enroll Student in Multiple Courses ---")
            try:
                student_id = int(input("Enter Student ID: "))
                courses_input = input("Enter Course IDs separated by commas (e.g., CS101, MATH201, ENG301): ")

                # បំបែក Course IDs តាមសញ្ញាក្បៀស និងលុបចន្លោះទទេរ (Whitespace)
                course_ids = [c.strip() for c in courses_input.split(",") if c.strip()]

                if not course_ids:
                    print("⚠️ No valid course IDs provided.")
                else:
                    success_count = 0
                    for c_id in course_ids:
                        # ធ្វើការ Enroll ចូល Graph ម្តងមួយៗ
                        admin_service.enroll_student(student_id, c_id)
                        success_count += 1

                    print(
                        f"SUCCESS: Enrolled Student ID {student_id} into {success_count} course(s): {', '.join(course_ids)}")
            except ValueError:
                print("⚠️ Invalid input. Student ID must be a number.")

        else:
            print("Invalid choice")


def show_student_menu(student_id):
    while True:
        print("\n" + "-" * 45)
        print(" " * 14 + "STUDENT MENU")
        print("-" * 45)
        print("\n1. View Profile.")
        print("2. View Registered courses.")
        print("3. Go back to Main Menu.")
        print("=" * 40)
        print("Welcome to Student Menu")
        print("=" * 40)
        print("\n1. View Profile & My Courses.")
        print("2. Go back to Main Menu.")

        choice = input("Enter your choice for student menu: ")

        if choice == "1":
            student = admin_service.get_student(student_id)

            if student:
                print("\n" + "=" * 50)
                print("      🎓 MY PROFILE & COURSES")
                print("=" * 50)
                print(f"ID:    {student['student_id']}")
                print(f"Name:  {student['name']}")
                print(f"Email: {student['email']}")
                print(f"Year:  {student['year']}")
                print(f"GPA:   {student['gpa']}")
                print("-" * 50)
                print("📚 Enrolled Courses:")

                enrolled_course_ids = admin_service.enrollment_graph.get_neighbors(student_id)

                if not enrolled_course_ids:
                    print("   [No courses registered yet]")
                else:
                    for course_id in enrolled_course_ids:
                        try:
                            formatted_course_id = int(course_id)
                        except (ValueError, TypeError):
                            formatted_course_id = course_id

                        course = admin_service.get_course(formatted_course_id)
                        if course:
                            # បង្ហាញជា Course Code យ៉ាងស្អាត
                            print(f"   - Course Code: {course.course_id} | {course.title}")
                        else:
                            print(f"   - Course Code: {course_id} (Details missing)")

                print("=" * 50 + "\n")
            else:
                print("\nError: Profile not found in database.\n")

        elif choice == "2":
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