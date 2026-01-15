"""
Data models for the Python CLI To-Do List Application.
"""

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
from datetime import datetime
import json
import os
import hashlib


class Priority(Enum):
    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Status(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class TodoItem:
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    details: str = ""
    priority: Priority = Priority.MID
    status: Status = Status.PENDING
    owner: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class AuthManager:
    """Manages user authentication (sign up and login) with JSON storage."""

    USERS_FILE = "users.json"

    def __init__(self, data_dir: str = "."):
        """Initialize AuthManager with a data directory."""
        self.data_dir = data_dir
        self.users_file_path = os.path.join(data_dir, self.USERS_FILE)
        self._ensure_users_file()

    def _ensure_users_file(self):
        """Create users.json if it doesn't exist."""
        if not os.path.exists(self.users_file_path):
            with open(self.users_file_path, "w") as f:
                json.dump({}, f)

    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def _load_users(self) -> dict:
        """Load users from JSON file."""
        try:
            with open(self.users_file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_users(self, users: dict):
        """Save users to JSON file."""
        with open(self.users_file_path, "w") as f:
            json.dump(users, f, indent=2)

    def sign_up(self, username: str, password: str) -> tuple[bool, str]:
        """
        Register a new user.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password cannot be empty."

        users = self._load_users()

        if username in users:
            return False, "Username already exists. Please choose a different one."

        users[username] = {"password": self._hash_password(password)}
        self._save_users(users)
        return True, f"Sign up successful! Welcome, {username}!"

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """
        Authenticate a user.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password cannot be empty."

        users = self._load_users()

        if username not in users:
            return False, "Username not found. Please sign up first."

        hashed_password = self._hash_password(password)
        if users[username]["password"] != hashed_password:
            return False, "Incorrect password. Please try again."

        return True, f"Login successful! Welcome, {username}!"


class TodoManager:
    """Manages todo items with JSON storage."""

    TODOS_FILE = "todos.json"

    def __init__(self, data_dir: str = "."):
        """Initialize TodoManager with a data directory."""
        self.data_dir = data_dir
        self.todos_file_path = os.path.join(data_dir, self.TODOS_FILE)
        self._ensure_todos_file()

    def _ensure_todos_file(self):
        """Create todos.json if it doesn't exist."""
        if not os.path.exists(self.todos_file_path):
            with open(self.todos_file_path, "w") as f:
                json.dump([], f)

    def _load_todos(self) -> list[dict]:
        """Load todos from JSON file."""
        try:
            with open(self.todos_file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_todos(self, todos: list[dict]):
        """Save todos to JSON file."""
        with open(self.todos_file_path, "w") as f:
            json.dump(todos, f, indent=2)

    def get_all_todos(self) -> list[TodoItem]:
        """Get all todos from the system."""
        todos_data = self._load_todos()
        all_todos = []
        for todo in todos_data:
            # Convert string values back to enums
            todo_dict = todo.copy()
            todo_dict["priority"] = Priority(todo["priority"])
            todo_dict["status"] = Status(todo["status"])
            all_todos.append(TodoItem(**todo_dict))
        return all_todos

    def get_user_todos(self, username: str) -> list[TodoItem]:
        """Get all todos for a user."""
        todos_data = self._load_todos()
        user_todos = []
        for todo in todos_data:
            if todo.get("owner") == username:
                # Convert string values back to enums
                todo_dict = todo.copy()
                todo_dict["priority"] = Priority(todo["priority"])
                todo_dict["status"] = Status(todo["status"])
                user_todos.append(TodoItem(**todo_dict))
        return user_todos

    def add_todo(self, todo: TodoItem) -> bool:
        """Add a new todo item."""
        todos_data = self._load_todos()
        todos_data.append(
            {
                "id": todo.id,
                "title": todo.title,
                "details": todo.details,
                "priority": todo.priority.value,
                "status": todo.status.value,
                "owner": todo.owner,
                "created_at": todo.created_at,
                "updated_at": todo.updated_at,
            }
        )
        self._save_todos(todos_data)
        return True

    def update_todo(self, todo_id: str, updated_todo: TodoItem) -> bool:
        """Update an existing todo item."""
        todos_data = self._load_todos()
        for i, todo in enumerate(todos_data):
            if todo["id"] == todo_id:
                updated_data = {
                    "id": updated_todo.id,
                    "title": updated_todo.title,
                    "details": updated_todo.details,
                    "priority": updated_todo.priority.value,
                    "status": updated_todo.status.value,
                    "owner": updated_todo.owner,
                    "created_at": updated_todo.created_at,
                    "updated_at": updated_todo.updated_at,
                }
                todos_data[i] = updated_data
                self._save_todos(todos_data)
                return True
        return False

    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item."""
        todos_data = self._load_todos()
        todos_data = [todo for todo in todos_data if todo["id"] != todo_id]
        self._save_todos(todos_data)
        return True

    def get_todo_by_id(self, todo_id: str) -> TodoItem | None:
        """Get a specific todo item by ID.

        Returns:
            TodoItem if found, None otherwise
        """
        todos_data = self._load_todos()
        for todo in todos_data:
            if todo["id"] == todo_id:
                # Convert string values back to enums
                todo_dict = todo.copy()
                todo_dict["priority"] = Priority(todo["priority"])
                todo_dict["status"] = Status(todo["status"])
                return TodoItem(**todo_dict)
        return None

    def mark_as_completed(self, todo_id: str) -> bool:
        """Mark a specific todo item as completed.

        Args:
            todo_id: The ID of the todo item to mark as completed

        Returns:
            bool: True if successfully marked as completed, False otherwise
        """
        todo = self.get_todo_by_id(todo_id)
        if todo is None:
            return False

        # Update the status to COMPLETED and update the timestamp
        updated_todo = TodoItem(
            id=todo.id,
            title=todo.title,
            details=todo.details,
            priority=todo.priority,
            status=Status.COMPLETED,
            owner=todo.owner,
            created_at=todo.created_at,
            updated_at=datetime.utcnow().isoformat(),
        )
        return self.update_todo(todo_id, updated_todo)
