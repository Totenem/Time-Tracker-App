import pytest
from lib.normalize_inputs import normalize_username, normalize_email

class TestNormalizeInputs:
    """Test cases for input normalization functions"""

    def test_normalize_username_valid_alphanumeric(self):
        """Test normalizing valid alphanumeric username"""
        username = "TestUser123"
        result = normalize_username(username)
        
        assert result == "testuser123"
        assert result.islower()

    def test_normalize_username_with_whitespace(self):
        """Test normalizing username with leading/trailing whitespace"""
        username = "  TestUser  "
        result = normalize_username(username)
        
        assert result == "testuser"
        assert result.strip() == result

    def test_normalize_username_lowercase(self):
        """Test normalizing already lowercase username"""
        username = "testuser"
        result = normalize_username(username)
        
        assert result == "testuser"

    def test_normalize_username_numbers_only(self):
        """Test normalizing username with numbers only"""
        username = "123456"
        result = normalize_username(username)
        
        assert result == "123456"

    def test_normalize_username_letters_only(self):
        """Test normalizing username with letters only"""
        username = "TestUser"
        result = normalize_username(username)
        
        assert result == "testuser"

    def test_normalize_username_invalid_special_characters(self):
        """Test normalizing username with special characters"""
        username = "test@user"
        
        with pytest.raises(ValueError, match="Username must contain only letters and numbers"):
            normalize_username(username)

    def test_normalize_username_invalid_spaces(self):
        """Test normalizing username with spaces in the middle"""
        username = "test user"
        
        with pytest.raises(ValueError, match="Username must contain only letters and numbers"):
            normalize_username(username)

    def test_normalize_username_empty_string(self):
        """Test normalizing empty username"""
        username = ""
        
        with pytest.raises(ValueError):
            normalize_username(username)

    def test_normalize_email_valid(self):
        """Test normalizing valid email"""
        email = "Test@Example.COM"
        result = normalize_email(email)
        
        assert result == "test@example.com"
        assert result.islower()

    def test_normalize_email_with_whitespace(self):
        """Test normalizing email with leading/trailing whitespace"""
        email = "  test@example.com  "
        result = normalize_email(email)
        
        assert result == "test@example.com"
        assert result.strip() == result

    def test_normalize_email_already_lowercase(self):
        """Test normalizing already lowercase email"""
        email = "test@example.com"
        result = normalize_email(email)
        
        assert result == "test@example.com"

    def test_normalize_email_with_subdomain(self):
        """Test normalizing email with subdomain"""
        email = "Test@Mail.Example.COM"
        result = normalize_email(email)
        
        assert result == "test@mail.example.com"

    def test_normalize_email_with_plus(self):
        """Test normalizing email with plus sign"""
        email = "test+tag@example.com"
        result = normalize_email(email)
        
        assert result == "test+tag@example.com"

    def test_normalize_email_with_dots(self):
        """Test normalizing email with dots"""
        email = "test.user@example.com"
        result = normalize_email(email)
        
        assert result == "test.user@example.com"

    def test_normalize_email_invalid_no_at(self):
        """Test normalizing invalid email without @"""
        email = "testexample.com"
        
        with pytest.raises(ValueError, match="Email is not valid"):
            normalize_email(email)

    def test_normalize_email_invalid_no_domain(self):
        """Test normalizing invalid email without domain"""
        email = "test@"
        
        with pytest.raises(ValueError, match="Email is not valid"):
            normalize_email(email)

    def test_normalize_email_invalid_no_tld(self):
        """Test normalizing invalid email without TLD"""
        email = "test@example"
        
        with pytest.raises(ValueError, match="Email is not valid"):
            normalize_email(email)

    def test_normalize_email_empty_string(self):
        """Test normalizing empty email"""
        email = ""
        
        with pytest.raises(ValueError):
            normalize_email(email)
