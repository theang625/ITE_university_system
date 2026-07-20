from services.admin_service import AdminService
from data import admins, students
from models.student import Student
from dsa.hash_table import HashTable
import json

admin_service = AdminService()


def show_main_menu():
    print("1. Admin Menu.")
    print("2. Student Menu.")
    print("3. Exit.")


def login(username, password):
    for i in range(len(admins)):
        if admins[i]["username"] == username and admins[i]["password"] == password:
            print(f"Login successful. Welcome, {admins[i]['username']} (admin ID {i})")
            show_admin_menu()
            return True  # Fixed: changed from 'return bool' to 'return True'

    print("Invalid username or password")
    return False


# --- NEW FUNCTION ADDED HERE ---
def student_login(username, password):
    file_path = "Userstudent.json"

    try:
        with open(file_path, "r") as f:
            users = json.load(f)

        for user in users:
            if user.get("username") == username and user.get("password") == password:
                print(f"\nLogin successful! Welcome, {username}.")

                # UPGRADE: Pass the actual student ID to the menu!
                linked_id = user.get("linked_student_id")
                show_student_menu(linked_id)

                return True

        print("\nInvalid username or password. Please try again.")
        return False

    except FileNotFoundError:
        print(f"Error: Could not find {file_path}. Please check the file name.")
        return False


# -------------------------------

def get_admins():
    with open("admins.json", "r") as f:
        admins_data = json.load(f)

    for admin in admins_data:
        print(f"Username: {admin['username']}")
    return show_main_menu()


def show_admin_menu():
    while True:
        print("=" * 30)
        print(" " * 4, end=" ")
        print("Welcome to Admin Menu")
        print("=" * 30)
        print("\nAdmin Menu")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Update Student")
        print("4. View Students")
        print("5. Enter student ID to search")
        print("6. Delete Course")
        print("7. Logout")

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
            print("=" * 35)

        elif choice == "5":
            student_id = int(input("Enter student ID to search: "))
            student = admin_service.get_student(student_id)
            if student:
                print("=" * 35)
                print(f"ID: {student['student_id']}")
                print(f"Name: {student['name']}")
                print(f"Email: {student['email']}")
                print(f"Year: {student['year']}")
                print(f"GPA: {student['gpa']}")
                print("=" * 35)
            else:
                print(f"Student ID {student_id} not found.")

        elif choice == "":
            course_id = input("Enter course ID: ")
            title = input("Enter course title: ")
            credits = int(input("Enter credits: "))
            admin_service.add_course(course_id, title, credits)
            print("Course added successfully")

        elif choice == "6":
            course_id = input("Enter course ID to delete: ")
            admin_service.delete_course(course_id)
            print("Course deleted successfully")

        elif choice == "7":
            print("Logged out")
            break

        else:
            print("Invalid choice")


# Add student_id as a parameter
def show_student_menu(student_id):
    while True:
        print("=" * 40)
        print("Welcome to Student Menu")
        print("=" * 40)
        print("\n1. View Profile.")
        print("2. View Registered courses.")
        print("3. Go back to Main Menu.")

        choice = input("Enter your choice for student menu: ")

        if choice == "1":
            # REPLACED PLACEHOLDER: Fetch and display actual data!
            student = admin_service.get_student(student_id)
            if student:
                print("\n" + "=" * 25)
                print("      MY PROFILE")
                print("=" * 25)
                print(f"ID:    {student['student_id']}")
                print(f"Name:  {student['name']}")
                print(f"Email: {student['email']}")
                print(f"Year:  {student['year']}")
                print(f"GPA:   {student['gpa']}")
                print("=" * 25 + "\n")
            else:
                print("\nError: Profile not found in database.\n")


        elif choice == "2":

            print("\n" + "=" * 35)

            print("      MY REGISTERED COURSES")

            print("=" * 35)

            # Step 1: Use the Graph to get the list of enrolled course IDs

            enrolled_course_ids = admin_service.enrollment_graph.get_neighbors(student_id)

            if not enrolled_course_ids:

                print("You are not registered for any courses yet.")

            else:

                # Step 2: Use the Binary Tree to get the full course details

                for course_id in enrolled_course_ids:

                    course = admin_service.get_course(course_id)

                    if course:

                        print(f"- [{course.course_id}] {course.title} ({course.credits} Credits)")

                    else:

                        print(f"- Course ID: {course_id} (Details not found in system)")

            print("=" * 35 + "\n")


def get_student():
    print("Student List.")
    print("=" * 35)
    with open("students.json", "r") as f:
        students_data = json.load(f)
    for student in students_data:
        print(f"Student: id: {student['id']}, name: {student['name']}")