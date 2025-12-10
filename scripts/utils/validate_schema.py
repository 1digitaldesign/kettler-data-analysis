#!/usr/bin/env python3
"""
Schema Validation Script

Validates FK/PK relationships, data types, constraints, and referential integrity
for all data files according to data/schema.json.

Uses Python 3.14 features: modern type hints, except expressions, efficient patterns.

Usage:
    python scripts/utils/validate_schema.py [--file <file_path>] [--table <table_name>] [--verbose]
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Any, Optional
from collections import defaultdict
import argparse

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import (
    PROJECT_ROOT, DATA_DIR, DATA_SOURCE_DIR, DATA_CLEANED_DIR,
    RESEARCH_DIR, RESEARCH_CONNECTIONS_DIR
)


class SchemaValidator:
    """Validates data against schema definition."""

    def __init__(self, schema_path: Path):
        """Initialize validator with schema file."""
        self.schema_path = schema_path
        self.schema = self._load_schema()
        self.errors = []
        self.warnings = []
        self.stats = {
            "files_validated": 0,
            "records_validated": 0,
            "errors_found": 0,
            "warnings_found": 0
        }

    def _load_schema(self) -> dict[str, Any]:
        """Load schema from JSON file."""
        try:
            return json.loads(self.schema_path.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"Error loading schema: {e}")
            sys.exit(1)

    def validate_license_number(self, value: Any, field_name: str) -> tuple[bool, Optional[str]]:
        """Validate license number format (10 digits)."""
        if value is None:
            return True, None

        if not isinstance(value, str):
            return False, f"{field_name} must be a string"

        if not re.match(r'^[0-9]{10}$', value):
            return False, f"{field_name} must be exactly 10 digits, got: {value}"

        return True, None

    def validate_state_code(self, value: Any, field_name: str) -> tuple[bool, Optional[str]]:
        """Validate state code format (2 uppercase letters)."""
        if value is None:
            return True, None

        if not isinstance(value, str):
            return False, f"{field_name} must be a string"

        if not re.match(r'^[A-Z]{2}$', value):
            return False, f"{field_name} must be 2 uppercase letters, got: {value}"

        return True, None

    def validate_date(self, value: Any, field_name: str) -> tuple[bool, Optional[str]]:
        """Validate date format (YYYY-MM-DD)."""
        if value is None:
            return True, None

        if not isinstance(value, str):
            return False, f"{field_name} must be a string"

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            return False, f"{field_name} must be in YYYY-MM-DD format, got: {value}"

        # Try to parse the date using except expression (PEP 758)
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return False, f"{field_name} is not a valid date: {value}"

        return True, None

    def validate_field(self, value: Any, field_def: dict[str, Any], field_name: str, record_id: Any = None) -> tuple[bool, Optional[str]]:
        """Validate a single field against its definition."""
        # Check required fields
        if field_def.get('required', False) and value is None:
            return False, f"{field_name} is required but missing"

        if value is None:
            return True, None

        # Check type
        expected_type = field_def.get('type')
        if expected_type:
            type_map = {
                'string': str,
                'integer': int,
                'number': (int, float),
                'boolean': bool,
                'array': list,
                'object': dict
            }
            expected_python_type = type_map.get(expected_type)
            if expected_python_type and not isinstance(value, expected_python_type):
                return False, f"{field_name} must be {expected_type}, got {type(value).__name__}"

        # Check format-specific validators
        format_type = field_def.get('format')
        if format_type == 'license_number':
            return self.validate_license_number(value, field_name)
        elif format_type == 'state_code':
            return self.validate_state_code(value, field_name)
        elif format_type == 'date':
            return self.validate_date(value, field_name)

        # Check enum values
        enum_values = field_def.get('enum')
        if enum_values and value not in enum_values:
            return False, f"{field_name} must be one of {enum_values}, got: {value}"

        return True, None

    def validate_record(self, record: dict[str, Any], table_def: dict[str, Any], record_id: Any = None) -> list[str]:
        """Validate a single record against table definition."""
        errors = []
        fields = table_def.get('fields', {})

        for field_name, field_def in fields.items():
            value = record.get(field_name)
            is_valid, error_msg = self.validate_field(value, field_def, field_name, record_id)
            if not is_valid:
                errors.append(error_msg)

        return errors

    def validate_primary_key(self, records: list[dict[str, Any]], pk_field: str) -> list[str]:
        """Validate primary key uniqueness."""
        errors = []
        seen_values = set()
        pk_values = defaultdict(list)

        for idx, record in enumerate(records):
            pk_value = record.get(pk_field)
            if pk_value is None:
                errors.append(f"Record {idx}: Primary key {pk_field} is missing")
                continue

            if pk_value in seen_values:
                pk_values[pk_value].append(idx)
            else:
                seen_values.add(pk_value)
                pk_values[pk_value] = [idx]

        # Report duplicates
        for pk_value, indices in pk_values.items():
            if len(indices) > 1:
                errors.append(f"Primary key {pk_field}={pk_value} appears {len(indices)} times at indices {indices}")

        return errors

    def validate_foreign_key(self, records: list[dict[str, Any]], fk_field: str, referenced_table: str, referenced_field: str) -> list[str]:
        """Validate foreign key referential integrity."""
        errors = []
        # Load referenced table
        referenced_records = self._load_referenced_table(referenced_table)
        if referenced_records is None:
            return [f"Cannot validate FK {fk_field}: Referenced table {referenced_table} not found"]

        referenced_values = {record.get(referenced_field) for record in referenced_records if record.get(referenced_field) is not None}

        for idx, record in enumerate(records):
            fk_value = record.get(fk_field)
            if fk_value is not None and fk_value not in referenced_values:
                errors.append(f"Record {idx}: FK {fk_field}={fk_value} not found in {referenced_table}.{referenced_field}")

        return errors

    def _load_referenced_table(self, table_name: str) -> Optional[list[dict[str, Any]]]:
        """Load a referenced table for FK validation."""
        # Try common locations
        possible_paths = [
            DATA_SOURCE_DIR / f"{table_name}.json",
            DATA_CLEANED_DIR / f"{table_name}.json",
            RESEARCH_CONNECTIONS_DIR / f"{table_name}.json",
        ]

        for path in possible_paths:
            if path.exists():
                try:
                    data = json.loads(path.read_text(encoding='utf-8'))
                    return data if isinstance(data, list) else [data] if isinstance(data, dict) else None
                except Exception:
                    continue

        return None

    def validate_file(self, file_path: Path, table_name: Optional[str] = None) -> dict[str, Any]:
        """Validate a single data file."""
        result = {
            'file': str(file_path),
            'valid': True,
            'errors': [],
            'warnings': [],
            'records_validated': 0
        }

        try:
            data = json.loads(file_path.read_text(encoding='utf-8'))
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Failed to load JSON: {e}")
            return result

        # Determine table name if not provided
        if not table_name:
            table_name = file_path.stem

        # Get table definition from schema
        tables = self.schema.get('tables', {})
        if table_name not in tables:
            result['warnings'].append(f"Table {table_name} not found in schema")
            return result

        table_def = tables[table_name]
        records = data if isinstance(data, list) else [data] if isinstance(data, dict) else []

        # Validate primary key
        pk_field = table_def.get('primary_key')
        if pk_field:
            pk_errors = self.validate_primary_key(records, pk_field)
            result['errors'].extend(pk_errors)

        # Validate foreign keys
        fk_defs = table_def.get('foreign_keys', [])
        for fk_def in fk_defs:
            fk_errors = self.validate_foreign_key(
                records,
                fk_def['field'],
                fk_def['references']['table'],
                fk_def['references']['field']
            )
            result['errors'].extend(fk_errors)

        # Validate each record
        for idx, record in enumerate(records):
            record_errors = self.validate_record(record, table_def, idx)
            result['errors'].extend(record_errors)
            result['records_validated'] += 1

        result['valid'] = len(result['errors']) == 0
        self.stats['files_validated'] += 1
        self.stats['records_validated'] += result['records_validated']
        self.stats['errors_found'] += len(result['errors'])
        self.stats['warnings_found'] += len(result['warnings'])

        return result

    def validate_all(self, data_dir: Path) -> dict[str, Any]:
        """Validate all data files in a directory."""
        results = {}
        json_files = list(data_dir.rglob('*.json'))

        for json_file in json_files:
            result = self.validate_file(json_file)
            results[str(json_file.relative_to(PROJECT_ROOT))] = result

        return results


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Validate data files against schema")
    parser.add_argument('--file', type=Path, help='Specific file to validate')
    parser.add_argument('--table', type=str, help='Table name for validation')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--schema', type=Path, default=DATA_DIR / 'schema.json', help='Schema file path')

    args = parser.parse_args()

    validator = SchemaValidator(args.schema)

    if args.file:
        result = validator.validate_file(args.file, args.table)
        print(f"\nValidation results for {args.file}:")
        print(f"Valid: {result['valid']}")
        print(f"Records validated: {result['records_validated']}")
        if result['errors']:
            print(f"\nErrors ({len(result['errors'])}):")
            for error in result['errors']:
                print(f"  - {error}")
        if result['warnings']:
            print(f"\nWarnings ({len(result['warnings'])}):")
            for warning in result['warnings']:
                print(f"  - {warning}")
    else:
        results = validator.validate_all(DATA_DIR)
        print(f"\nValidation Summary:")
        print(f"Files validated: {validator.stats['files_validated']}")
        print(f"Records validated: {validator.stats['records_validated']}")
        print(f"Errors found: {validator.stats['errors_found']}")
        print(f"Warnings found: {validator.stats['warnings_found']}")

        if args.verbose:
            for file_path, result in results.items():
                if not result['valid']:
                    print(f"\n{file_path}:")
                    for error in result['errors']:
                        print(f"  - {error}")

    return 0 if validator.stats['errors_found'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
