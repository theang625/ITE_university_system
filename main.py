from utils.menu import show_admin_menu, show_main_menu, show_student_menu, login, get_student, student_login
import json


def main():
    print("=" * 45)
    print("UNIVERSITY MANAGEMENT SYSTEM".center(45))
    print("=" * 45)

    while True:
        show_main_menu()
        choice = input("\n Enter your choice: ").strip()

        if choice == "1":
            print("\n" + "-" * 45)
            print(" " * 14 + "ADMIN LOGIN")
            print("-" * 45)
            username = input("Username: ")
            password = input("Password: ")
            login(username, password)

        elif choice == "2":
            print("\n" + "-" * 45)
            print(" " * 13 + "STUDENT LOGIN")
            print("-" * 45)
            username = input("Username: ")
            password = input("Password: ")
            student_login(username, password)

        elif choice == "3":
            print("\n" + "=" * 45)
            print(" " * 12 + "Thank you for using")
            print(" " * 10 + "the University System!")
            print("=" * 45)
            break

        else:
            print("\n Invalid choice. Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()