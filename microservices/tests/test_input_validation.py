"""
Comprehensive Input Validation Tests
Tests all input validation scenarios
"""

import pytest
from utils.validation import (
    validate_string, validate_integer, validate_list, validate_dict,
    validate_email, validate_phone, validate_license_number,
    validate_address, validate_borough, validate_block_lot,
    validate_json_payload, sanitize_input, validate_pagination,
    validate_uuid, ValidationError
)


class TestStringValidation:
    """Test string validation"""

    def test_valid_string(self):
        """Test valid string"""
        result = validate_string("test", "field")
        assert result == "test"

    def test_too_short(self):
        """Test string too short"""
        with pytest.raises(ValidationError):
            validate_string("", "field", min_length=1)

    def test_too_long(self):
        """Test string too long"""
        with pytest.raises(ValidationError):
            validate_string("a" * 1001, "field", max_length=1000)

    def test_not_string(self):
        """Test non-string input"""
        with pytest.raises(ValidationError):
            validate_string(123, "field")


class TestIntegerValidation:
    """Test integer validation"""

    def test_valid_integer(self):
        """Test valid integer"""
        result = validate_integer(123, "field")
        assert result == 123

    def test_below_minimum(self):
        """Test integer below minimum"""
        with pytest.raises(ValidationError):
            validate_integer(5, "field", min_value=10)

    def test_above_maximum(self):
        """Test integer above maximum"""
        with pytest.raises(ValidationError):
            validate_integer(100, "field", max_value=50)

    def test_string_to_integer(self):
        """Test string conversion to integer"""
        result = validate_integer("123", "field")
        assert result == 123


class TestListValidation:
    """Test list validation"""

    def test_valid_list(self):
        """Test valid list"""
        result = validate_list([1, 2, 3], "field")
        assert result == [1, 2, 3]

    def test_too_few_items(self):
        """Test list with too few items"""
        with pytest.raises(ValidationError):
            validate_list([], "field", min_items=1)

    def test_too_many_items(self):
        """Test list with too many items"""
        with pytest.raises(ValidationError):
            validate_list([1] * 1001, "field", max_items=1000)

    def test_not_list(self):
        """Test non-list input"""
        with pytest.raises(ValidationError):
            validate_list("not a list", "field")


class TestEmailValidation:
    """Test email validation"""

    def test_valid_email(self):
        """Test valid email"""
        result = validate_email("test@example.com")
        assert result == "test@example.com"

    def test_invalid_email(self):
        """Test invalid email"""
        with pytest.raises(ValidationError):
            validate_email("not-an-email")

    def test_missing_at(self):
        """Test email without @"""
        with pytest.raises(ValidationError):
            validate_email("testexample.com")


class TestPhoneValidation:
    """Test phone validation"""

    def test_valid_phone(self):
        """Test valid phone"""
        result = validate_phone("703-555-1234")
        assert len(result) >= 10

    def test_invalid_phone(self):
        """Test invalid phone"""
        with pytest.raises(ValidationError):
            validate_phone("123")


class TestLicenseValidation:
    """Test license number validation"""

    def test_valid_license(self):
        """Test valid license"""
        result = validate_license_number("12345678")
        assert result == "12345678"

    def test_invalid_license(self):
        """Test invalid license"""
        with pytest.raises(ValidationError):
            validate_license_number("12345")  # Too short


class TestAddressValidation:
    """Test address validation"""

    def test_valid_address(self):
        """Test valid address"""
        result = validate_address("123 Main Street, Alexandria, VA 22314")
        assert len(result) > 0

    def test_too_short(self):
        """Test address too short"""
        with pytest.raises(ValidationError):
            validate_address("123")

    def test_no_street(self):
        """Test address without street"""
        with pytest.raises(ValidationError):
            validate_address("Alexandria, VA")


class TestBoroughValidation:
    """Test borough validation"""

    def test_valid_borough(self):
        """Test valid borough"""
        result = validate_borough("Manhattan")
        assert result == "Manhattan"

    def test_invalid_borough(self):
        """Test invalid borough"""
        with pytest.raises(ValidationError):
            validate_borough("Invalid")


class TestSanitization:
    """Test input sanitization"""

    def test_sanitize_string(self):
        """Test string sanitization"""
        result = sanitize_input("<script>alert('xss')</script>", "string")
        assert "<script>" not in result

    def test_sanitize_integer(self):
        """Test integer sanitization"""
        result = sanitize_input("123", "integer")
        assert result == 123


class TestPaginationValidation:
    """Test pagination validation"""

    def test_valid_pagination(self):
        """Test valid pagination"""
        page, page_size = validate_pagination(1, 10)
        assert page == 1
        assert page_size == 10

    def test_invalid_page(self):
        """Test invalid page"""
        with pytest.raises(ValidationError):
            validate_pagination(0, 10)  # Page must be >= 1


class TestUUIDValidation:
    """Test UUID validation"""

    def test_valid_uuid(self):
        """Test valid UUID"""
        result = validate_uuid("123e4567-e89b-12d3-a456-426614174000")
        assert len(result) == 36

    def test_invalid_uuid(self):
        """Test invalid UUID"""
        with pytest.raises(ValidationError):
            validate_uuid("not-a-uuid")
