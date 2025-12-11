#!/usr/bin/env python3
"""
State and Jurisdiction Normalization Utility

Normalizes state names and jurisdiction identifiers to ensure data consistency.
Maps variations like "dc" to "dc" and handles other state name formats.
"""

from typing import Dict, Any, Union, List
import re
from pathlib import Path


# Comprehensive state name mappings
STATE_NORMALIZATION_MAP = {
    # District of Columbia variations
    "dc": "dc",
    "district_of_columbia": "dc",
    "district of columbia": "dc",
    "District of Columbia": "dc",
    "DISTRICT OF COLUMBIA": "dc",
    "D.C.": "dc",
    "D.C": "dc",
    "DC": "dc",

    # Standard state abbreviations (already normalized)
    "al": "al", "ak": "ak", "az": "az", "ar": "ar", "ca": "ca",
    "co": "co", "ct": "ct", "de": "de", "fl": "fl", "ga": "ga",
    "hi": "hi", "id": "id", "il": "il", "in": "in", "ia": "ia",
    "ks": "ks", "ky": "ky", "la": "la", "me": "me", "md": "md",
    "ma": "ma", "mi": "mi", "mn": "mn", "ms": "ms", "mo": "mo",
    "mt": "mt", "ne": "ne", "nv": "nv", "nh": "nh", "nj": "nj",
    "nm": "nm", "ny": "ny", "nc": "nc", "nd": "nd", "oh": "oh",
    "ok": "ok", "or": "or", "pa": "pa", "ri": "ri", "sc": "sc",
    "sd": "sd", "tn": "tn", "tx": "tx", "ut": "ut", "vt": "vt",
    "va": "va", "wa": "wa", "wv": "wv", "wi": "wi", "wy": "wy",

    # Full state names to abbreviations
    "alabama": "al", "alaska": "ak", "arizona": "az", "arkansas": "ar",
    "california": "ca", "colorado": "co", "connecticut": "ct", "delaware": "de",
    "florida": "fl", "georgia": "ga", "hawaii": "hi", "idaho": "id",
    "illinois": "il", "indiana": "in", "iowa": "ia", "kansas": "ks",
    "kentucky": "ky", "louisiana": "la", "maine": "me", "maryland": "md",
    "massachusetts": "ma", "michigan": "mi", "minnesota": "mn", "mississippi": "ms",
    "missouri": "mo", "montana": "mt", "nebraska": "ne", "nevada": "nv",
    "new hampshire": "nh", "new jersey": "nj", "new mexico": "nm", "new york": "ny",
    "north carolina": "nc", "north dakota": "nd", "ohio": "oh", "oklahoma": "ok",
    "oregon": "or", "pennsylvania": "pa", "rhode island": "ri", "south carolina": "sc",
    "south dakota": "sd", "tennessee": "tn", "texas": "tx", "utah": "ut",
    "vermont": "vt", "virginia": "va", "washington": "wa", "west virginia": "wv",
    "wisconsin": "wi", "wyoming": "wy",

    # Title case variations
    "Alabama": "al", "Alaska": "ak", "Arizona": "az", "Arkansas": "ar",
    "California": "ca", "Colorado": "co", "Connecticut": "ct", "Delaware": "de",
    "Florida": "fl", "Georgia": "ga", "Hawaii": "hi", "Idaho": "id",
    "Illinois": "il", "Indiana": "in", "Iowa": "ia", "Kansas": "ks",
    "Kentucky": "ky", "Louisiana": "la", "Maine": "me", "Maryland": "md",
    "Massachusetts": "ma", "Michigan": "mi", "Minnesota": "mn", "Mississippi": "ms",
    "Missouri": "mo", "Montana": "mt", "Nebraska": "ne", "Nevada": "nv",
    "New Hampshire": "nh", "New Jersey": "nj", "New Mexico": "nm", "New York": "ny",
    "North Carolina": "nc", "North Dakota": "nd", "Ohio": "oh", "Oklahoma": "ok",
    "Oregon": "or", "Pennsylvania": "pa", "Rhode Island": "ri", "South Carolina": "sc",
    "South Dakota": "sd", "Tennessee": "tn", "Texas": "tx", "Utah": "ut",
    "Vermont": "vt", "Virginia": "va", "Washington": "wa", "West Virginia": "wv",
    "Wisconsin": "wi", "Wyoming": "wy",
}


def normalize_state(state: Union[str, None]) -> str:
    """
    Normalize a state name or abbreviation to lowercase abbreviation.

    Args:
        state: State name, abbreviation, or variation

    Returns:
        Normalized lowercase state abbreviation (e.g., "dc", "va", "tx")
    """
    if not state:
        return ""

    # Convert to string and strip whitespace
    state_str = str(state).strip()

    # Handle empty strings
    if not state_str:
        return ""

    # Handle uppercase 2-letter codes first (e.g., "VA", "TX", "DC")
    if len(state_str) == 2 and state_str.isupper() and state_str.isalpha():
        return state_str.lower()

    # If already a 2-letter lowercase code, return as-is
    if len(state_str) == 2 and state_str.islower() and state_str.isalpha():
        return state_str

    # Try direct lookup first (preserve original case variations)
    original_str = state_str
    if original_str in STATE_NORMALIZATION_MAP:
        return STATE_NORMALIZATION_MAP[original_str]

    # Normalize to lowercase for lookup
    state_lower = state_str.lower()
    if state_lower in STATE_NORMALIZATION_MAP:
        return STATE_NORMALIZATION_MAP[state_lower]

    # Normalize separators (underscores, hyphens, spaces) and try again
    state_normalized = re.sub(r'[_\s-]+', '_', state_lower)
    if state_normalized in STATE_NORMALIZATION_MAP:
        return STATE_NORMALIZATION_MAP[state_normalized]

    # Try original string with underscores (for cases like "district_of_columbia")
    if state_str in STATE_NORMALIZATION_MAP:
        return STATE_NORMALIZATION_MAP[state_str]

    # Try with spaces replaced by underscores
    state_underscore = state_lower.replace(' ', '_').replace('-', '_')
    if state_underscore in STATE_NORMALIZATION_MAP:
        return STATE_NORMALIZATION_MAP[state_underscore]

    # Try title case variations
    state_title = state_str.title()
    if state_title in STATE_NORMALIZATION_MAP:
        return STATE_NORMALIZATION_MAP[state_title]

    # If it's a 2-letter code that got here, return lowercase
    if len(state_str) == 2 and state_str.isalpha():
        return state_str.lower()

    # Return normalized lowercase version if no match found
    return state_normalized if state_normalized else state_lower


def normalize_jurisdiction(jurisdiction: Union[str, None]) -> str:
    """
    Normalize jurisdiction identifier (alias for normalize_state for consistency).

    Args:
        jurisdiction: Jurisdiction name or identifier

    Returns:
        Normalized lowercase jurisdiction abbreviation
    """
    return normalize_state(jurisdiction)


def normalize_dict_recursive(data: Any, depth: int = 0, max_depth: int = 50) -> Any:
    """
    Recursively normalize state/jurisdiction fields in a dictionary or list.

    Args:
        data: Dictionary, list, or primitive value to normalize
        depth: Current recursion depth
        max_depth: Maximum recursion depth to prevent infinite loops

    Returns:
        Normalized data structure
    """
    if depth > max_depth:
        return data

    if isinstance(data, dict):
        normalized = {}
        for key, value in data.items():
            # Normalize the key if it is a state identifier
            normalized_key = key
            if isinstance(key, str):
                # Direct lookup in normalization map
                if key in STATE_NORMALIZATION_MAP:
                    normalized_key = STATE_NORMALIZATION_MAP[key]
                # Handle uppercase 2-letter state codes directly
                elif len(key) == 2 and key.isupper() and key.isalpha():
                    normalized_key = key.lower()
                else:
                    # Try normalizing the key
                    key_normalized = normalize_state(key)
                    # If normalization changed the key and it's a valid state abbreviation, use it
                    if key_normalized != key and (key_normalized in STATE_NORMALIZATION_MAP.values() or
                                                 (len(key_normalized) == 2 and key_normalized.isalpha())):
                        normalized_key = key_normalized

            # Normalize the value - be more aggressive
            if isinstance(value, str):
                # Try to normalize any string value that might be a state
                normalized_value = normalize_state(value)
                # If normalization didn't change it, recursively process
                if normalized_value == value:
                    normalized_value = normalize_dict_recursive(value, depth + 1, max_depth)
            else:
                # Recursively process non-string values
                normalized_value = normalize_dict_recursive(value, depth + 1, max_depth)

            normalized[normalized_key] = normalized_value

        return normalized

    elif isinstance(data, list):
        return [normalize_dict_recursive(item, depth + 1, max_depth) for item in data]

    elif isinstance(data, str):
        # Normalize string values directly
        return normalize_state(data)

    else:
        return data


def find_state_fields(data: Any, path: str = "", found: List[str] = None) -> List[str]:
    """
    Find all paths to fields that might contain state/jurisdiction data.

    Args:
        data: Data structure to search
        path: Current path in the structure
        found: List of found paths

    Returns:
        List of paths to potential state/jurisdiction fields
    """
    if found is None:
        found = []

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key

            # Check if key suggests state/jurisdiction
            key_lower = str(key).lower()
            if any(indicator in key_lower for indicator in ['state', 'jurisdiction', 'location', 'region', 'abbreviation']):
                found.append(current_path)

            # Check if value looks like a state
            if isinstance(value, str) and len(value) <= 50:
                value_lower = value.lower()
                if (value_lower in STATE_NORMALIZATION_MAP or
                    value_lower.replace('_', ' ') in STATE_NORMALIZATION_MAP or
                    (len(value) == 2 and value.isalpha())):
                    found.append(current_path)

            # Recurse
            find_state_fields(value, current_path, found)

    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]" if path else f"[{i}]"
            find_state_fields(item, current_path, found)

    return found


if __name__ == "__main__":
    # Test normalization
    test_cases = [
        "dc",
        "dc",
        "D.C.",
        "DC",
        "dc",
        "virginia",
        "VA",
        "va",
        "texas",
        "TX",
    ]

    print("State Normalization Test:")
    for test in test_cases:
        normalized = normalize_state(test)
        print(f"  '{test}' -> '{normalized}'")
