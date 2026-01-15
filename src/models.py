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
            with open(self.users_file_path, 'w') as f:
                json.dump({}, f)
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self) -> dict:
        """Load users from JSON file."""
        try:
            with open(self.users_file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_users(self, users: dict):
        """Save users to JSON file."""
        with open(self.users_file_path, 'w') as f:
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
        
        users[username] = {
            "password": self._hash_password(password)
        }
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
