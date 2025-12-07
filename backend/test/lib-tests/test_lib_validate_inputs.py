import pytest
from fastapi.responses import JSONResponse
from lib.validate_inputs import validate_password

class TestValidateInputs:
    """Test cases for input validation functions"""

    def test_validate_password_valid(self):
        """Test validating a valid password"""
        password = "TestPassword123"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        assert result.body.decode() == '{"message":"Password is valid"}'

    def test_validate_password_too_short(self):
        """Test validating password that is too short"""
        password = "Test123"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 400
        assert "at least 8 characters" in result.body.decode().lower()

    def test_validate_password_no_uppercase(self):
        """Test validating password without uppercase letter"""
        password = "testpassword123"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 400
        assert "uppercase" in result.body.decode().lower()

    def test_validate_password_no_lowercase(self):
        """Test validating password without lowercase letter"""
        password = "TESTPASSWORD123"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 400
        assert "lowercase" in result.body.decode().lower()

    def test_validate_password_no_number(self):
        """Test validating password without number"""
        password = "TestPassword"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 400
        assert "number" in result.body.decode().lower()

    def test_validate_password_exactly_8_characters(self):
        """Test validating password with exactly 8 characters"""
        password = "Test1234"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200

    def test_validate_password_long_valid(self):
        """Test validating a long valid password"""
        password = "VeryLongTestPassword123456"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200

    def test_validate_password_with_special_characters(self):
        """Test validating password with special characters"""
        password = "TestPass123!"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200

    def test_validate_password_multiple_numbers(self):
        """Test validating password with multiple numbers"""
        password = "TestPassword12345"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200

    def test_validate_password_multiple_uppercase(self):
        """Test validating password with multiple uppercase letters"""
        password = "TESTPassword123"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200

    def test_validate_password_empty_string(self):
        """Test validating empty password"""
        password = ""
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 400
        assert "at least 8 characters" in result.body.decode().lower()

    def test_validate_password_only_numbers(self):
        """Test validating password with only numbers"""
        password = "12345678"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 400

    def test_validate_password_only_letters(self):
        """Test validating password with only letters"""
        password = "TestPassword"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 400

    def test_validate_password_only_lowercase_and_numbers(self):
        """Test validating password with lowercase and numbers only"""
        password = "test12345"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 400

    def test_validate_password_only_uppercase_and_numbers(self):
        """Test validating password with uppercase and numbers only"""
        password = "TEST12345"
        result = validate_password(password)
        
        assert isinstance(result, JSONResponse)
        assert result.status_code == 400
