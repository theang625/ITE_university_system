from services.admin_service import AdminService
from data import admins
import json 

admin_service = AdminService()

def show_main_menu():
    print("1. Admin Menu")
    print("2. Stdent Menu")
    print("3. View Admin")
    print("4. View Student")
    print("5. Exit")
    
def login(username, password):
        for i in range(len(admins)):
            if admins[i]["username"] == username and admins[i]["password"] == password:
                print(f"Login successful. Welcome, {admins[i]['username']} (admin ID {i})")
                return admins[i]  # or return i, whatever you need
        
        print("Invalid username or password")

        return None
    
def get_admins() :
    
    with open("admins.json", "r") as f:
        admins = json.load(f)
    for admin in admins:
        print(f"Username: {admin['username']}")
    return show_main_menu()
        
def show_admin_menu():
    
    print("=" * 30)
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
    
    choice = input("Enter your choice for admin menu: ")
    
    while True:
        
        if choice == "1":
            student_id = int(input("Enter student ID: "))
            name = input("Enter student name: ")
            email = input("Enter student email: ")
            gpa = input("Enter student GPA: ")
            admin_service.add_student(student_id, name,email, gpa)
            print("Student added successfully")
                    
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
            break
        else:
            print("Invalid choice")
            
def show_student_menu():
    print("=" * 40)
    print("Welcome to Student Menu")
    print("=" * 40)
    print("\n1. View Profile.")
    print("2. View Regitstered courses.")
