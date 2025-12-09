"""
Comprehensive Input Validation
Production-grade validation for all microservices
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, validator, Field
import re
from datetime import datetime
import json


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_string(value: Any, field_name: str, min_length: int = 1, max_length: int = 1000) -> str:
    """Validate string input"""
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string")
    if len(value.strip()) < min_length:
        raise ValidationError(f"{field_name} must be at least {min_length} characters")
    if len(value) > max_length:
        raise ValidationError(f"{field_name} must be at most {max_length} characters")
    return value.strip()


def validate_integer(value: Any, field_name: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    """Validate integer input"""
    if not isinstance(value, int):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be an integer")

    if min_value is not None and value < min_value:
        raise ValidationError(f"{field_name} must be at least {min_value}")
    if max_value is not None and value > max_value:
        raise ValidationError(f"{field_name} must be at most {max_value}")

    return value


def validate_list(value: Any, field_name: str, min_items: int = 0, max_items: int = 1000) -> List:
    """Validate list input"""
    if not isinstance(value, list):
        raise ValidationError(f"{field_name} must be a list")
    if len(value) < min_items:
        raise ValidationError(f"{field_name} must have at least {min_items} items")
    if len(value) > max_items:
        raise ValidationError(f"{field_name} must have at most {max_items} items")
    return value


def validate_dict(value: Any, field_name: str, required_keys: Optional[List[str]] = None) -> Dict:
    """Validate dictionary input"""
    if not isinstance(value, dict):
        raise ValidationError(f"{field_name} must be a dictionary")

    if required_keys:
        missing = [key for key in required_keys if key not in value]
        if missing:
            raise ValidationError(f"{field_name} missing required keys: {', '.join(missing)}")

    return value


def validate_email(email: str) -> str:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")
    return email


def validate_phone(phone: str) -> str:
    """Validate phone number format"""
    # Remove common formatting
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    pattern = r'^\d{10,15}$'
    if not re.match(pattern, cleaned):
        raise ValidationError("Invalid phone number format")
    return cleaned


def validate_license_number(license: str) -> str:
    """Validate license number format"""
    cleaned = license.strip()
    pattern = r'^\d{6,8}$'
    if not re.match(pattern, cleaned):
        raise ValidationError("License number must be 6-8 digits")
    return cleaned


def validate_address(address: str) -> str:
    """Validate address format"""
    if len(address.strip()) < 10:
        raise ValidationError("Address too short")
    if len(address) > 500:
        raise ValidationError("Address too long")

    # Check for required components
    has_street = any(word in address.lower() for word in ['street', 'st', 'avenue', 'ave', 'road', 'rd', 'drive', 'dr', 'lane', 'ln', 'way', 'blvd', 'boulevard'])
    if not has_street:
        raise ValidationError("Address must include street name")

    return address.strip()


def validate_borough(borough: str) -> str:
    """Validate NYC borough"""
    valid_boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
    if borough not in valid_boroughs:
        raise ValidationError(f"Borough must be one of: {', '.join(valid_boroughs)}")
    return borough


def validate_block_lot(block: str, lot: str) -> tuple:
    """Validate block and lot numbers"""
    block_cleaned = block.strip()
    lot_cleaned = lot.strip()

    if not re.match(r'^\d+$', block_cleaned):
        raise ValidationError("Block must be numeric")
    if not re.match(r'^\d+$', lot_cleaned):
        raise ValidationError("Lot must be numeric")

    return block_cleaned, lot_cleaned


def validate_json_payload(payload: Any) -> Dict:
    """Validate JSON payload"""
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format")

    if not isinstance(payload, dict):
        raise ValidationError("Payload must be a dictionary")

    return payload


def sanitize_input(value: Any, input_type: str = "string") -> Any:
    """Sanitize input to prevent injection attacks"""
    if input_type == "string" and isinstance(value, str):
        # Remove potentially dangerous characters
        value = re.sub(r'[<>"\']', '', value)
        value = value.strip()
    elif input_type == "integer":
        value = validate_integer(value, "value")
    elif input_type == "list":
        value = validate_list(value, "value")

    return value


def validate_pagination(page: int, page_size: int) -> tuple:
    """Validate pagination parameters"""
    page = validate_integer(page, "page", min_value=1, max_value=10000)
    page_size = validate_integer(page_size, "page_size", min_value=1, max_value=100)
    return page, page_size


def validate_uuid(uuid_str: str) -> str:
    """Validate UUID format"""
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(pattern, uuid_str.lower()):
        raise ValidationError("Invalid UUID format")
    return uuid_str.lower()
