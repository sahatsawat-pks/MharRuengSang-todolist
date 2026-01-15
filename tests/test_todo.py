"""
Unit tests for the TodoManager todo management module.
"""

import pytest
import json
import os
import tempfile
from src.models import TodoManager, TodoItem, Priority, Status


class TestTodoManager:
    """Test suite for TodoManager class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield tmp_dir

    @pytest.fixture
    def todo_manager(self, temp_dir):
        """Create a TodoManager instance with a temporary directory."""
        return TodoManager(data_dir=temp_dir)

    # Initialization Tests

    def test_init_creates_todos_file(self, temp_dir):
        """Test that TodoManager creates todos.json on initialization."""
        TodoManager(data_dir=temp_dir)
        todos_file = os.path.join(temp_dir, "todos.json")
        assert os.path.exists(todos_file)
        with open(todos_file, "r") as f:
            assert json.load(f) == []

    # Get User Todos Tests

    def test_get_user_todos_empty(self, todo_manager):
        """Test getting todos for a user with no todos."""
        todos = todo_manager.get_user_todos("user1")
        assert todos == []

    def test_get_user_todos_with_todos(self, todo_manager):
        """Test getting todos for a user with existing todos."""
        todo1 = TodoItem(title="Test Todo 1", owner="user1")
        todo2 = TodoItem(title="Test Todo 2", owner="user1")
        todo3 = TodoItem(title="Test Todo 3", owner="user2")
        todo_manager.add_todo(todo1)
        todo_manager.add_todo(todo2)
        todo_manager.add_todo(todo3)

        user1_todos = todo_manager.get_user_todos("user1")
        user2_todos = todo_manager.get_user_todos("user2")

        assert len(user1_todos) == 2
        assert len(user2_todos) == 1
        assert user1_todos[0].title == "Test Todo 1"
        assert user1_todos[1].title == "Test Todo 2"
        assert user2_todos[0].title == "Test Todo 3"

    # Add Todo Tests

    def test_add_todo(self, todo_manager):
        """Test adding a new todo."""
        todo = TodoItem(
            title="New Todo", details="Details", priority=Priority.HIGH, owner="user1"
        )
        result = todo_manager.add_todo(todo)
        assert result is True

        todos = todo_manager.get_user_todos("user1")
        assert len(todos) == 1
        assert todos[0].title == "New Todo"
        assert todos[0].details == "Details"
        assert todos[0].priority == Priority.HIGH
        assert todos[0].status == Status.PENDING
        assert todos[0].owner == "user1"

    def test_add_todo_persistence(self, temp_dir):
        """Test that added todos persist across instances."""
        manager1 = TodoManager(data_dir=temp_dir)
        todo = TodoItem(title="Persistent Todo", owner="user1")
        manager1.add_todo(todo)

        manager2 = TodoManager(data_dir=temp_dir)
        todos = manager2.get_user_todos("user1")
        assert len(todos) == 1
        assert todos[0].title == "Persistent Todo"

    # Update Todo Tests

    def test_update_todo_existing(self, todo_manager):
        """Test updating an existing todo."""
        todo = TodoItem(
            title="Original",
            details="Original details",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="user1",
        )
        todo_manager.add_todo(todo)
        original_id = todo.id

        updated_todo = TodoItem(
            id=original_id,
            title="Updated",
            details="Updated details",
            priority=Priority.HIGH,
            status=Status.COMPLETED,
            owner="user1",
            created_at=todo.created_at,
            updated_at="2023-01-01T00:00:00",
        )
        result = todo_manager.update_todo(original_id, updated_todo)
        assert result is True

        todos = todo_manager.get_user_todos("user1")
        assert len(todos) == 1
        assert todos[0].title == "Updated"
        assert todos[0].details == "Updated details"
        assert todos[0].priority == Priority.HIGH
        assert todos[0].status == Status.COMPLETED
        assert todos[0].updated_at == "2023-01-01T00:00:00"

    def test_update_todo_nonexistent(self, todo_manager):
        """Test updating a non-existent todo."""
        todo = TodoItem(title="Test", owner="user1")
        result = todo_manager.update_todo("nonexistent_id", todo)
        assert result is False

    # Delete Todo Tests

    def test_delete_todo_existing(self, todo_manager):
        """Test deleting an existing todo."""
        todo = TodoItem(title="To Delete", owner="user1")
        todo_manager.add_todo(todo)
        original_id = todo.id

        result = todo_manager.delete_todo(original_id)
        assert result is True

        todos = todo_manager.get_user_todos("user1")
        assert len(todos) == 0

    def test_delete_todo_nonexistent(self, todo_manager):
        """Test deleting a non-existent todo."""
        result = todo_manager.delete_todo("nonexistent_id")
        assert result is True  # Delete is idempotent

    # Integration Tests

    def test_multiple_users_multiple_todos(self, todo_manager):
        """Test multiple users with multiple todos."""
        # User 1 todos
        todo1 = TodoItem(title="User1 Todo1", owner="user1", priority=Priority.HIGH)
        todo2 = TodoItem(title="User1 Todo2", owner="user1", priority=Priority.LOW)

        # User 2 todos
        todo3 = TodoItem(title="User2 Todo1", owner="user2", priority=Priority.MID)

        todo_manager.add_todo(todo1)
        todo_manager.add_todo(todo2)
        todo_manager.add_todo(todo3)

        user1_todos = todo_manager.get_user_todos("user1")
        user2_todos = todo_manager.get_user_todos("user2")

        assert len(user1_todos) == 2
        assert len(user2_todos) == 1

        # Update user1's first todo
        updated_todo1 = TodoItem(
            id=todo1.id,
            title="Updated User1 Todo1",
            owner="user1",
            priority=Priority.HIGH,
            created_at=todo1.created_at,
        )
        todo_manager.update_todo(todo1.id, updated_todo1)

        user1_todos = todo_manager.get_user_todos("user1")
        assert user1_todos[0].title == "Updated User1 Todo1"

        # Delete user2's todo
        todo_manager.delete_todo(todo3.id)
        user2_todos = todo_manager.get_user_todos("user2")
        assert len(user2_todos) == 0
