from services.admin_service import AdminService
from data import admins, students
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
                return bool  # or return i, whatever you need
        
        print("Invalid username or password")

        return None
    
def get_admins() :
    
    with open("admins.json", "r") as f:
        admins = json.load(f)
        
    for admin in admins:
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
        print("5. Add Course")
        print("6. Delete Course")
        print("7. Logout")

        choice = input("Enter your choice for admin menu: ")  # moved inside loop, asked every time

        if choice == "1":
            student_id = int(input("Enter student ID: "))
            name = str(input("Enter student name: "))
            email = str(input("Enter student email: "))
            year = int(input("Enter student year: "))
            gpa = float(input("Enter student GPA: "))

            result = admin_service.add_student(student_id, name, email, year, gpa)
            if result is not None:
                print("Student added successfully")
            # no recursive call here — the while loop just naturally repeats

        elif choice == "2":
            student_id = int(input("Enter student ID to delete: "))
            admin_service.delete_student(student_id)
            print("Student deleted successfully")

        elif choice == "3":
            student_id = int(input("Enter student ID to update: "))
            name = input("Enter new name (leave blank to keep): ")
            email = input("Enter new email (leave blank to keep): ")
            admin_service.update_student(student_id, name or None, email or None)
            print("Student updated successfully")

        elif choice == "4":
            for student in admin_service.view_students():
                print(student)

        elif choice == "5":
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
            break   # this is what actually returns control to show_main_menu()

        else:
            print("Invalid choice")
            
def show_student_menu():
    print("=" * 40)
    print("Welcome to Student Menu")
    print("=" * 40)
    print("\n1. View Profile.")
    print("2. View Regitstered courses.")
    
def get_student():
    print("Student List.")
    print("=" * 35)
    with open("students.json", "r") as f:
        students = json.load(f)  # renamed, and loop over this
    for student in students:
        print(f"Student: id: {student['id']}, name: {student['name']}")
        
    
