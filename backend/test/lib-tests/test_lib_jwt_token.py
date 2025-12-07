import pytest
from unittest.mock import patch, MagicMock
import jwt
from lib.jwt_token import generate_jwt_token, verify_jwt_token
import os

class TestJWTToken:
    """Test cases for JWT token generation and verification"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.test_secret = "test_secret_key"
        self.test_payload = {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "email": "test@example.com"
        }

    @patch('lib.jwt_token.token_secret', 'test_secret_key')
    def test_generate_jwt_token_success(self):
        """Test successful JWT token generation"""
        token = generate_jwt_token(self.test_payload)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    @patch('lib.jwt_token.token_secret', 'test_secret_key')
    def test_generate_jwt_token_contains_payload(self):
        """Test that generated token contains the payload"""
        token = generate_jwt_token(self.test_payload)
        decoded = jwt.decode(token, 'test_secret_key', algorithms=["HS256"])
        
        assert decoded["user_id"] == self.test_payload["user_id"]
        assert decoded["username"] == self.test_payload["username"]
        assert decoded["email"] == self.test_payload["email"]

    @patch('lib.jwt_token.token_secret', 'test_secret_key')
    def test_verify_jwt_token_success(self):
        """Test successful JWT token verification"""
        token = generate_jwt_token(self.test_payload)
        decoded = verify_jwt_token(token)
        
        assert decoded["user_id"] == self.test_payload["user_id"]
        assert decoded["username"] == self.test_payload["username"]
        assert decoded["email"] == self.test_payload["email"]

    @patch('lib.jwt_token.token_secret', 'test_secret_key')
    def test_verify_jwt_token_invalid_token(self):
        """Test JWT token verification with invalid token"""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(jwt.InvalidTokenError):
            verify_jwt_token(invalid_token)

    @patch('lib.jwt_token.token_secret', 'test_secret_key')
    def test_verify_jwt_token_wrong_secret(self):
        """Test JWT token verification with wrong secret"""
        token = generate_jwt_token(self.test_payload)
        
        with patch('lib.jwt_token.token_secret', 'wrong_secret'):
            with pytest.raises(jwt.InvalidSignatureError):
                verify_jwt_token(token)

    @patch('lib.jwt_token.token_secret', 'test_secret_key')
    def test_generate_jwt_token_empty_payload(self):
        """Test JWT token generation with empty payload"""
        empty_payload = {}
        token = generate_jwt_token(empty_payload)
        
        assert token is not None
        assert isinstance(token, str)

    @patch('lib.jwt_token.token_secret', 'test_secret_key')
    def test_generate_and_verify_roundtrip(self):
        """Test that generated token can be verified correctly"""
        token = generate_jwt_token(self.test_payload)
        decoded = verify_jwt_token(token)
        
        assert decoded == self.test_payload
