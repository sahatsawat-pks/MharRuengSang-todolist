"""
Entry point for the Python CLI To-Do List Application.
"""

def main():
    print("Welcome to the Python CLI To-Do List Application!")
    while True:
        print("\n--- Main Menu ---")
        print("[1] Login")
        print("[2] Sign Up")
        print("[3] Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            print("Login selected (not yet implemented), please check back soon.")
        elif choice == "2":
            print("Sign Up selected (not yet implemented), please check back soon.")
        elif choice == "3":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
