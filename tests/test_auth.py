"""
Unit tests for the AuthManager authentication module.
"""

import pytest
import json
import os
import tempfile
from pathlib import Path
from src.models import AuthManager


class TestAuthManager:
    """Test suite for AuthManager class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield tmp_dir
    
    @pytest.fixture
    def auth_manager(self, temp_dir):
        """Create an AuthManager instance with a temporary directory."""
        return AuthManager(data_dir=temp_dir)
    
    # Sign Up Tests
    
    def test_sign_up_successful(self, auth_manager):
        """Test successful user sign up."""
        success, message = auth_manager.sign_up("john_doe", "secure_password")
        assert success is True
        assert "Sign up successful" in message
    
    def test_sign_up_duplicate_username(self, auth_manager):
        """Test sign up with duplicate username."""
        auth_manager.sign_up("john_doe", "password1")
        success, message = auth_manager.sign_up("john_doe", "password2")
        assert success is False
        assert "already exists" in message
    
    def test_sign_up_empty_username(self, auth_manager):
        """Test sign up with empty username."""
        success, message = auth_manager.sign_up("", "password123")
        assert success is False
        assert "cannot be empty" in message
    
    def test_sign_up_empty_password(self, auth_manager):
        """Test sign up with empty password."""
        success, message = auth_manager.sign_up("john_doe", "")
        assert success is False
        assert "cannot be empty" in message
    
    def test_sign_up_empty_both(self, auth_manager):
        """Test sign up with empty username and password."""
        success, message = auth_manager.sign_up("", "")
        assert success is False
        assert "cannot be empty" in message
    
    def test_sign_up_creates_json_file(self, auth_manager, temp_dir):
        """Test that sign up creates the users.json file."""
        auth_manager.sign_up("testuser", "password123")
        users_file = Path(temp_dir) / "users.json"
        assert users_file.exists()
    
    def test_sign_up_stores_data_in_json(self, auth_manager, temp_dir):
        """Test that sign up data is correctly stored in JSON."""
        auth_manager.sign_up("alice", "secret_pass")
        users_file = Path(temp_dir) / "users.json"
        
        with open(users_file, 'r') as f:
            users = json.load(f)
        
        assert "alice" in users
        assert "password" in users["alice"]
    
    def test_sign_up_password_is_hashed(self, auth_manager, temp_dir):
        """Test that passwords are hashed, not stored in plain text."""
        password = "plain_text_password"
        auth_manager.sign_up("bob", password)
        users_file = Path(temp_dir) / "users.json"
        
        with open(users_file, 'r') as f:
            users = json.load(f)
        
        stored_password = users["bob"]["password"]
        assert stored_password != password
        assert len(stored_password) == 64  # SHA-256 hash length
    
    def test_sign_up_multiple_users(self, auth_manager, temp_dir):
        """Test signing up multiple users."""
        auth_manager.sign_up("user1", "pass1")
        auth_manager.sign_up("user2", "pass2")
        auth_manager.sign_up("user3", "pass3")
        
        users_file = Path(temp_dir) / "users.json"
        with open(users_file, 'r') as f:
            users = json.load(f)
        
        assert len(users) == 3
        assert "user1" in users
        assert "user2" in users
        assert "user3" in users
    
    # Login Tests
    
    def test_login_successful(self, auth_manager):
        """Test successful login with correct credentials."""
        auth_manager.sign_up("john_doe", "correct_password")
        success, message = auth_manager.login("john_doe", "correct_password")
        assert success is True
        assert "Login successful" in message
    
    def test_login_wrong_password(self, auth_manager):
        """Test login with wrong password."""
        auth_manager.sign_up("john_doe", "correct_password")
        success, message = auth_manager.login("john_doe", "wrong_password")
        assert success is False
        assert "Incorrect password" in message
    
    def test_login_nonexistent_user(self, auth_manager):
        """Test login with non-existent username."""
        success, message = auth_manager.login("nonexistent", "password")
        assert success is False
        assert "not found" in message
    
    def test_login_empty_username(self, auth_manager):
        """Test login with empty username."""
        success, message = auth_manager.login("", "password")
        assert success is False
        assert "cannot be empty" in message
    
    def test_login_empty_password(self, auth_manager):
        """Test login with empty password."""
        success, message = auth_manager.login("john_doe", "")
        assert success is False
        assert "cannot be empty" in message
    
    def test_login_empty_both(self, auth_manager):
        """Test login with empty username and password."""
        success, message = auth_manager.login("", "")
        assert success is False
        assert "cannot be empty" in message
    
    def test_login_case_sensitive_username(self, auth_manager):
        """Test that login is case-sensitive for username."""
        auth_manager.sign_up("John_Doe", "password123")
        success, message = auth_manager.login("john_doe", "password123")
        assert success is False
    
    def test_login_case_sensitive_password(self, auth_manager):
        """Test that login is case-sensitive for password."""
        auth_manager.sign_up("john_doe", "Password123")
        success, message = auth_manager.login("john_doe", "password123")
        assert success is False
    
    # Integration Tests
    
    def test_sign_up_then_login(self, auth_manager):
        """Test the complete flow of signing up and then logging in."""
        # Sign up
        sign_up_success, sign_up_msg = auth_manager.sign_up("test_user", "test_pass")
        assert sign_up_success is True
        
        # Login
        login_success, login_msg = auth_manager.login("test_user", "test_pass")
        assert login_success is True
    
    def test_multiple_users_login(self, auth_manager):
        """Test multiple users can sign up and login independently."""
        users = [
            ("alice", "alice_pass"),
            ("bob", "bob_pass"),
            ("charlie", "charlie_pass")
        ]
        
        # Sign up all users
        for username, password in users:
            success, _ = auth_manager.sign_up(username, password)
            assert success is True
        
        # Each user logs in successfully
        for username, password in users:
            success, msg = auth_manager.login(username, password)
            assert success is True
    
    def test_users_file_persistence(self, temp_dir):
        """Test that user data persists across AuthManager instances."""
        # Create first instance and sign up a user
        auth1 = AuthManager(data_dir=temp_dir)
        auth1.sign_up("persist_user", "persist_pass")
        
        # Create second instance and verify user exists
        auth2 = AuthManager(data_dir=temp_dir)
        success, message = auth2.login("persist_user", "persist_pass")
        assert success is True
    
    def test_same_password_different_users(self, auth_manager):
        """Test that different users can have the same password."""
        password = "shared_password"
        auth_manager.sign_up("user1", password)
        auth_manager.sign_up("user2", password)
        
        # Both should be able to login
        success1, _ = auth_manager.login("user1", password)
        success2, _ = auth_manager.login("user2", password)
        
        assert success1 is True
        assert success2 is True
    
    def test_special_characters_in_credentials(self, auth_manager):
        """Test sign up and login with special characters."""
        username = "user@example.com"
        password = "P@ssw0rd!#$%"
        
        sign_up_success, _ = auth_manager.sign_up(username, password)
        assert sign_up_success is True
        
        login_success, _ = auth_manager.login(username, password)
        assert login_success is True
    
    def test_whitespace_in_credentials(self, auth_manager):
        """Test sign up and login with whitespace in credentials."""
        username = "user with spaces"
        password = "pass with spaces"
        
        sign_up_success, _ = auth_manager.sign_up(username, password)
        assert sign_up_success is True
        
        login_success, _ = auth_manager.login(username, password)
        assert login_success is True
    
    def test_long_credentials(self, auth_manager):
        """Test sign up and login with very long credentials."""
        username = "a" * 100
        password = "b" * 200
        
        sign_up_success, _ = auth_manager.sign_up(username, password)
        assert sign_up_success is True
        
        login_success, _ = auth_manager.login(username, password)
        assert login_success is True
