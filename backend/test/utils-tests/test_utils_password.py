import pytest
import bcrypt
from utils.password import hash_password, verify_password

class TestPasswordUtils:
    """Test cases for password hashing and verification utilities"""

    def test_hash_password_returns_bytes(self):
        """Test that hash_password returns bytes"""
        password = "TestPassword123"
        result = hash_password(password)
        
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_hash_password_different_hashes(self):
        """Test that same password produces different hashes (due to salt)"""
        password = "TestPassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Hashes should be different due to random salt
        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Test verifying a correct password"""
        password = "TestPassword123"
        hashed = hash_password(password)
        
        result = verify_password(password, hashed.decode('utf-8'))
        
        assert result is True

    def test_verify_password_incorrect(self):
        """Test verifying an incorrect password"""
        password = "TestPassword123"
        wrong_password = "WrongPassword123"
        hashed = hash_password(password)
        
        result = verify_password(wrong_password, hashed.decode('utf-8'))
        
        assert result is False

    def test_verify_password_empty_password(self):
        """Test verifying an empty password"""
        password = "TestPassword123"
        hashed = hash_password(password)
        
        result = verify_password("", hashed.decode('utf-8'))
        
        assert result is False

    def test_verify_password_empty_hash(self):
        """Test verifying password with empty hash"""
        password = "TestPassword123"
        
        with pytest.raises(Exception):
            verify_password(password, "")

    def test_hash_and_verify_roundtrip(self):
        """Test that hashed password can be verified correctly"""
        password = "TestPassword123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed.decode('utf-8')) is True

    def test_hash_password_special_characters(self):
        """Test hashing password with special characters"""
        password = "Test@Password#123$"
        hashed = hash_password(password)
        
        assert isinstance(hashed, bytes)
        assert verify_password(password, hashed.decode('utf-8')) is True

    def test_hash_password_unicode(self):
        """Test hashing password with unicode characters"""
        password = "TestPässwörd123"
        hashed = hash_password(password)
        
        assert isinstance(hashed, bytes)
        assert verify_password(password, hashed.decode('utf-8')) is True

    def test_hash_password_long_password(self):
        """Test hashing a long password"""
        password = "A" * 100 + "1"
        hashed = hash_password(password)
        
        assert isinstance(hashed, bytes)
        assert verify_password(password, hashed.decode('utf-8')) is True

    def test_hash_password_short_password(self):
        """Test hashing a short password"""
        password = "Test1"
        hashed = hash_password(password)
        
        assert isinstance(hashed, bytes)
        assert verify_password(password, hashed.decode('utf-8')) is True

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case sensitive"""
        password = "TestPassword123"
        hashed = hash_password(password)
        
        assert verify_password("testpassword123", hashed.decode('utf-8')) is False
        assert verify_password("TESTPASSWORD123", hashed.decode('utf-8')) is False
        assert verify_password("TestPassword123", hashed.decode('utf-8')) is True

    def test_hash_password_uses_bcrypt(self):
        """Test that hash_password uses bcrypt algorithm"""
        password = "TestPassword123"
        hashed = hash_password(password)
        
        # Bcrypt hashes start with $2b$ or $2a$ or $2y$
        hashed_str = hashed.decode('utf-8')
        assert hashed_str.startswith('$2')
