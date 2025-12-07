import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the backend directory to Python path so modules can be imported
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Load environment variables for testing
load_dotenv()

@pytest.fixture
def mock_db_connection():
    """Mock database connection for testing"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }

@pytest.fixture
def sample_jwt_payload():
    """Sample JWT payload for testing"""
    return {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "username": "testuser",
        "email": "test@example.com"
    }
