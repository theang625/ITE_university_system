from services.admin_service import AdminService
from data import admins, students
from models.student import Student
from dsa.hash_table import HashTable
from models.admin import Admin
from models.student import Student
import json 

admin_service = AdminService()

def show_main_menu():
    print("1. Admin Menu.")
    print("2. Student Menu.")
    print("3. Exit.")
    
def login(username, password):
    admins = Admin.load_admins()

    for i in range(len(admins)):
        if admins[i]["username"] == username and admins[i]["password"] == password:
            print(f"Login successful. Welcome, {admins[i]['username']} (admin ID {i})")
            show_admin_menu()
            return admins[i]  # return the matched admin dict, not bool

    print("Invalid username or password")
    return None
        
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

        choice = input("Enter your choice for admin menu: ")   # now asked every loop

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
            
def show_student_menu():
    
    while True:
        
        print("=" * 40)
        print("\tWelcome to Student Menu")
        print("=" * 40)
        print("\n1. View Profile.")
        print("2. View Regitstered courses.")
        print("3. Logout from your account.")
        
        choice = input("Enter your choice for student menu: ")
        
        if choice == "1":
            users = Student.load_users()
            students = Student.load_students()

            print("=" * 35)
            print("Login your account first.")
            student_user = input("Input your username: ")

            for i in range(len(users)):
                if users[i]['username'] == student_user:
                    user_password = input("Input your password: ")

                    if users[i]['password'] == user_password:
                        print("\tLogin successful.")
                        print(f"\tWelcome, {users[i]['username']}.")

                        # Find the matching student record by ID
                        logged_in_user = users[i]
                        matched_student = None

                        for s in students:
                            if s['student_id'] == logged_in_user['user_id']:
                                matched_student = s
                                break

                        if matched_student:
                            print("=" * 35)
                            print("Student Profile")
                            print("-" * 35)
                            print(f"ID:    {matched_student['student_id']}")
                            print(f"Name:  {matched_student['name']}")
                            print(f"Email: {matched_student['email']}")
                            print(f"Year:  {matched_student['year']}")
                            print(f"GPA:   {matched_student['gpa']}")
                            print("-" * 35)
                        else:
                            print("No matching student profile found.")

                        return logged_in_user

                    else:
                        print("\tInvalid password.")
                        return None

            print("\tInvalid username.")
            return None
        
        elif choice == "2": 
            pass
        
        elif choice == "3":
            print("Logged out")
            break
        
        else :
            print("Invalid choice")


        
    
