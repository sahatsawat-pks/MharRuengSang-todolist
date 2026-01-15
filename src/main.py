"""
Entry point for the Python CLI To-Do List Application.
"""

from models import AuthManager, TodoManager, TodoItem, Priority, Status
from datetime import datetime


class App:
    """Main application class for the CLI To-Do List."""

    def __init__(self):
        """Initialize the application."""
        self.auth_manager = AuthManager(data_dir=".")
        self.todo_manager = TodoManager(data_dir=".")
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
            print("[3] Edit Todo")
            print("[4] Logout")
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.handle_view_todos()
            elif choice == "2":
                self.handle_add_todo()
            elif choice == "3":
                self.handle_edit_todo()
            elif choice == "4":
                print(f"Logging out. Goodbye, {self.current_user}!")
                self.current_user = None
                break
            else:
                print("Invalid option. Please try again.")

    def handle_view_todos(self):
        """Handle viewing todos."""
        todos = self.todo_manager.get_user_todos(self.current_user)
        if not todos:
            print("No todos found.")
            return
        print("\n--- Your Todos ---")
        for i, todo in enumerate(todos, 1):
            print(
                f"[{i}] {todo.title} - {todo.status.value} - Priority: {todo.priority.value}"
            )
            print(f"    Details: {todo.details}")
            print(f"    Created: {todo.created_at}")
            print()

    def handle_add_todo(self):
        """Handle adding a new todo."""
        print("\n--- Add New Todo ---")
        title = input("Title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return
        details = input("Details: ").strip()
        priority_input = input("Priority (HIGH/MID/LOW, default MID): ").strip().upper()
        try:
            priority = (
                Priority[priority_input]
                if priority_input in Priority.__members__
                else Priority.MID
            )
        except KeyError:
            priority = Priority.MID

        todo = TodoItem(
            title=title, details=details, priority=priority, owner=self.current_user
        )
        self.todo_manager.add_todo(todo)
        print("Todo added successfully!")

    def handle_edit_todo(self):
        """Handle editing an existing todo."""
        todos = self.todo_manager.get_user_todos(self.current_user)
        if not todos:
            print("No todos to edit.")
            return
        self.handle_view_todos()
        try:
            choice = int(input("Enter the number of the todo to edit: ").strip())
            if 1 <= choice <= len(todos):
                todo = todos[choice - 1]
                print(f"\nEditing: {todo.title}")
                title = input(f"Title ({todo.title}): ").strip() or todo.title
                details = input(f"Details ({todo.details}): ").strip() or todo.details
                priority_input = (
                    input(f"Priority ({todo.priority.value}): ").strip().upper()
                )
                try:
                    priority = (
                        Priority[priority_input]
                        if priority_input in Priority.__members__
                        else todo.priority
                    )
                except KeyError:
                    priority = todo.priority
                status_input = input(f"Status ({todo.status.value}): ").strip().upper()
                try:
                    status = (
                        Status[status_input]
                        if status_input in Status.__members__
                        else todo.status
                    )
                except KeyError:
                    status = todo.status

                updated_todo = TodoItem(
                    id=todo.id,
                    title=title,
                    details=details,
                    priority=priority,
                    status=status,
                    owner=todo.owner,
                    created_at=todo.created_at,
                    updated_at=datetime.utcnow().isoformat(),
                )
                self.todo_manager.update_todo(todo.id, updated_todo)
                print("Todo updated successfully!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")


def main():
    """Main entry point."""
    print("Welcome to the Python CLI To-Do List Application!")
    app = App()
    app.display_pre_login_menu()


if __name__ == "__main__":
    main()
