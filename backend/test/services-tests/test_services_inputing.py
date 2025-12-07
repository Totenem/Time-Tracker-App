import pytest
from unittest.mock import patch, MagicMock
from services.inputing import store_user
from datetime import datetime

class TestInputingServices:
    """Test cases for input services"""

    @patch('services.inputing.connect_to_db')
    def test_store_user_success(self, mock_connect):
        """Test successfully storing a user"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        user_data = {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "email": "test@example.com",
            "password": "hashed_password",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        result = store_user(user_data)
        
        assert result is True
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('services.inputing.connect_to_db')
    def test_store_user_db_connection_failed(self, mock_connect):
        """Test storing user when database connection fails"""
        mock_connect.return_value = None
        
        user_data = {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "email": "test@example.com",
            "password": "hashed_password",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        result = store_user(user_data)
        
        assert result is False

    @patch('services.inputing.connect_to_db')
    def test_store_user_correct_parameters(self, mock_connect):
        """Test that store_user passes correct parameters to database"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        user_data = {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "email": "test@example.com",
            "password": "hashed_password",
            "created_at": datetime(2024, 1, 1, 0, 0, 0),
            "updated_at": datetime(2024, 1, 1, 0, 0, 0)
        }
        
        store_user(user_data)
        
        # Verify the execute call was made with correct SQL and parameters
        call_args = mock_cursor.execute.call_args
        assert call_args is not None
        sql_query = call_args[0][0]
        params = call_args[0][1]
        
        assert "INSERT INTO users" in sql_query
        assert params[0] == user_data["user_id"]
        assert params[1] == user_data["username"]
        assert params[2] == user_data["email"]
        assert params[3] == user_data["password"]
        assert params[4] == user_data["created_at"]
        assert params[5] == user_data["updated_at"]

    @patch('services.inputing.connect_to_db')
    def test_store_user_commits_transaction(self, mock_connect):
        """Test that store_user commits the transaction"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        user_data = {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "email": "test@example.com",
            "password": "hashed_password",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        store_user(user_data)
        
        # Verify commit was called
        mock_conn.commit.assert_called_once()

    @patch('services.inputing.connect_to_db')
    def test_store_user_with_different_user_data(self, mock_connect):
        """Test storing user with different user data"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        user_data = {
            "user_id": "987e6543-e21b-43d2-b654-321987654321",
            "username": "anotheruser",
            "email": "another@example.com",
            "password": "different_hashed_password",
            "created_at": datetime(2024, 2, 1, 12, 30, 0),
            "updated_at": datetime(2024, 2, 1, 12, 30, 0)
        }
        
        result = store_user(user_data)
        
        assert result is True
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
