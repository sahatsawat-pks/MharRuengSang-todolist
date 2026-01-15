"""
Entry point for the Python CLI To-Do List Application.
"""

from models import AuthManager


class App:
    """Main application class for the CLI To-Do List."""
    
    def __init__(self):
        """Initialize the application."""
        self.auth_manager = AuthManager(data_dir=".")
        self.current_user = None
    
    def display_pre_login_menu(self):
        """Display the main menu before login."""
        while True:
            print("\n--- Main Menu ---")
            print("[1] Login")
            print("[2] Sign Up")
            print("[3] Exit")
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_sign_up()
            elif choice == "3":
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
    
    def handle_login(self):
        """Handle user login."""
        print("\n--- Login ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        success, message = self.auth_manager.login(username, password)
        print(message)
        
        if success:
            self.current_user = username
            self.display_post_login_menu()
    
    def handle_sign_up(self):
        """Handle user sign up."""
        print("\n--- Sign Up ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        confirm_password = input("Confirm Password: ").strip()
        
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            return
        
        success, message = self.auth_manager.sign_up(username, password)
        print(message)
    
    def display_post_login_menu(self):
        """Display menu after successful login."""
        while True:
            print(f"\n--- Welcome, {self.current_user}! ---")
            print("[1] View Todos")
            print("[2] Add Todo")
            print("[3] Logout")
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                print("View Todos (not yet implemented)")
            elif choice == "2":
                print("Add Todo (not yet implemented)")
            elif choice == "3":
                print(f"Logging out. Goodbye, {self.current_user}!")
                self.current_user = None
                break
            else:
                print("Invalid option. Please try again.")


def main():
    """Main entry point."""
    print("Welcome to the Python CLI To-Do List Application!")
    app = App()
    app.display_pre_login_menu()


if __name__ == "__main__":
    main()
