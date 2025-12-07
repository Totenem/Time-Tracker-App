import pytest
import uuid
from utils.generate_uuid import generate_uuid

class TestGenerateUUID:
    """Test cases for UUID generation utility"""

    def test_generate_uuid_returns_string(self):
        """Test that generate_uuid returns a string"""
        result = generate_uuid()
        
        assert isinstance(result, str)
        assert len(result) > 0

    def test_generate_uuid_valid_format(self):
        """Test that generate_uuid returns a valid UUID format"""
        result = generate_uuid()
        
        # Try to parse it as a UUID to verify format
        parsed_uuid = uuid.UUID(result)
        assert str(parsed_uuid) == result

    def test_generate_uuid_unique(self):
        """Test that generate_uuid generates unique UUIDs"""
        uuid1 = generate_uuid()
        uuid2 = generate_uuid()
        uuid3 = generate_uuid()
        
        assert uuid1 != uuid2
        assert uuid2 != uuid3
        assert uuid1 != uuid3

    def test_generate_uuid_version_4(self):
        """Test that generate_uuid generates UUID version 4"""
        result = generate_uuid()
        parsed_uuid = uuid.UUID(result)
        
        assert parsed_uuid.version == 4

    def test_generate_uuid_multiple_calls(self):
        """Test generating multiple UUIDs in sequence"""
        uuids = [generate_uuid() for _ in range(10)]
        
        # All should be unique
        assert len(set(uuids)) == 10
        
        # All should be valid UUIDs
        for uid in uuids:
            uuid.UUID(uid)

    def test_generate_uuid_length(self):
        """Test that generate_uuid returns correct length"""
        result = generate_uuid()
        
        # UUID4 string representation is 36 characters (32 hex + 4 hyphens)
        assert len(result) == 36

    def test_generate_uuid_hex_characters(self):
        """Test that generate_uuid contains only valid hex characters and hyphens"""
        result = generate_uuid()
        
        # Remove hyphens and check if remaining are hex characters
        hex_part = result.replace('-', '')
        assert all(c in '0123456789abcdef' for c in hex_part.lower())
