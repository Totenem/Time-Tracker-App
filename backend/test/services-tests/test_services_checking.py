import pytest
from unittest.mock import patch, MagicMock
from services.checking import check_if_username_exists, check_if_email_exists
from fastapi.responses import JSONResponse

class TestCheckingServices:
    """Test cases for checking services"""

    @patch('services.checking.connect_to_db')
    def test_check_if_username_exists_true(self, mock_connect):
        """Test checking if username exists when it does exist"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("user_id", "testuser", "test@example.com")
        mock_connect.return_value = mock_conn
        
        result = check_if_username_exists("testuser")
        
        assert result is True
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE username = %s", ("testuser",))

    @patch('services.checking.connect_to_db')
    def test_check_if_username_exists_false(self, mock_connect):
        """Test checking if username exists when it doesn't exist"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value = mock_conn
        
        result = check_if_username_exists("nonexistent")
        
        assert result is False
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE username = %s", ("nonexistent",))

    @patch('services.checking.connect_to_db')
    def test_check_if_username_exists_db_connection_failed(self, mock_connect):
        """Test checking username when database connection fails"""
        mock_connect.return_value = None
        
        result = check_if_username_exists("testuser")
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 500
        assert "Database connection failed" in result.body.decode()

    @patch('services.checking.connect_to_db')
    def test_check_if_email_exists_true(self, mock_connect):
        """Test checking if email exists when it does exist"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("user_id", "testuser", "test@example.com")
        mock_connect.return_value = mock_conn
        
        result = check_if_email_exists("test@example.com")
        
        assert result is True
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE email = %s", ("test@example.com",))

    @patch('services.checking.connect_to_db')
    def test_check_if_email_exists_false(self, mock_connect):
        """Test checking if email exists when it doesn't exist"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value = mock_conn
        
        result = check_if_email_exists("nonexistent@example.com")
        
        assert result is False
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE email = %s", ("nonexistent@example.com",))

    @patch('services.checking.connect_to_db')
    def test_check_if_email_exists_db_connection_failed(self, mock_connect):
        """Test checking email when database connection fails"""
        mock_connect.return_value = None
        
        result = check_if_email_exists("test@example.com")
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 500
        assert "Database connection failed" in result.body.decode()

    @patch('services.checking.connect_to_db')
    def test_check_if_username_exists_normalized_input(self, mock_connect):
        """Test checking username with normalized input"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value = mock_conn
        
        result = check_if_username_exists("TestUser")
        
        assert result is False
        # Verify the exact username passed to the query
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE username = %s", ("TestUser",))

    @patch('services.checking.connect_to_db')
    def test_check_if_email_exists_normalized_input(self, mock_connect):
        """Test checking email with normalized input"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value = mock_conn
        
        result = check_if_email_exists("Test@Example.COM")
        
        assert result is False
        # Verify the exact email passed to the query
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE email = %s", ("Test@Example.COM",))
