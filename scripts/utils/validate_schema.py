#!/usr/bin/env python3
"""
Schema Validation Script

Validates FK/PK relationships, data types, constraints, and referential integrity
for all data files according to data/schema.json.

Usage:
    python scripts/utils/validate_schema.py [--file <file_path>] [--table <table_name>] [--verbose]
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
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

    def _load_schema(self) -> Dict[str, Any]:
        """Load schema from JSON file."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
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

        # Try to parse the date
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return False, f"{field_name} is not a valid date: {value}"

        return True, None

    def validate_field(self, value: Any, field_def: Dict[str, Any], field_name: str, record_id: Any = None) -> tuple[bool, Optional[str]]:
        """Validate a single field against its definition."""
        # Check required fields
        if field_def.get("required", False) and value is None:
            record_info = f" (record: {record_id})" if record_id else ""
            return False, f"{field_name} is required but missing{record_info}"

        # Skip validation if value is None and field is not required
        if value is None:
            return True, None

        # Check type
        expected_type = field_def.get("type")
        if expected_type:
            type_map = {
                "string": str,
                "number": (int, float),
                "boolean": bool,
                "array": list,
                "object": dict
            }

            if expected_type in type_map:
                expected_python_type = type_map[expected_type]
                if not isinstance(value, expected_python_type):
                    record_info = f" (record: {record_id})" if record_id else ""
                    return False, f"{field_name} must be {expected_type}, got {type(value).__name__}{record_info}"

        # Check format
        field_format = field_def.get("format")
        if field_format:
            if field_format.startswith("^[0-9]{10}$"):
                valid, error = self.validate_license_number(value, field_name)
                if not valid:
                    return False, error
            elif field_format.startswith("^[A-Z]{2}$"):
                valid, error = self.validate_state_code(value, field_name)
                if not valid:
                    return False, error
            elif field_format == "date" or field_format == "YYYY-MM-DD":
                valid, error = self.validate_date(value, field_name)
                if not valid:
                    return False, error

        # Check enum values
        enum_values = field_def.get("enum")
        if enum_values and value not in enum_values:
            record_info = f" (record: {record_id})" if record_id else ""
            return False, f"{field_name} must be one of {enum_values}, got: {value}{record_info}"

        return True, None

    def validate_record(self, record: Dict[str, Any], table_def: Dict[str, Any], record_index: int) -> List[str]:
        """Validate a single record against table definition."""
        errors = []
        pk_field = table_def.get("primary_key")

        # Get PK value for error reporting
        pk_value = record.get(pk_field) if pk_field else record_index

        # Validate all fields
        fields = table_def.get("fields", {})
        for field_name, field_def in fields.items():
            value = record.get(field_name)
            valid, error = self.validate_field(value, field_def, field_name, pk_value)
            if not valid:
                errors.append(error)

        # Validate primary key uniqueness (will be checked at table level)
        if pk_field:
            pk_value = record.get(pk_field)
            if pk_value is None:
                errors.append(f"Primary key {pk_field} is missing")

        return errors

    def validate_foreign_keys(self, records: List[Dict[str, Any]], table_def: Dict[str, Any],
                              all_tables_data: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Validate foreign key referential integrity."""
        errors = []
        fks = table_def.get("foreign_keys", [])

        if not fks:
            return errors

        pk_field = table_def.get("primary_key")
        table_name = None
        for tname, tdef in self.schema.get("tables", {}).items():
            if tdef == table_def:
                table_name = tname
                break

        for fk_def in fks:
            fk_field = fk_def.get("field")
            ref_table_field = fk_def.get("references", "")

            if "." not in ref_table_field:
                continue

            ref_table, ref_field = ref_table_field.split(".", 1)

            # Get referenced table data
            ref_table_data = all_tables_data.get(ref_table, [])
            ref_values = set()
            for ref_record in ref_table_data:
                ref_value = ref_record.get(ref_field)
                if ref_value is not None:
                    ref_values.add(ref_value)

            # Check FK values exist in referenced table
            for record in records:
                fk_value = record.get(fk_field)
                if fk_value is not None:  # FK is optional
                    if fk_value not in ref_values:
                        pk_value = record.get(pk_field, "unknown")
                        errors.append(
                            f"FK violation in {table_name}: {fk_field}={fk_value} "
                            f"references {ref_table}.{ref_field} but value not found "
                            f"(record PK: {pk_value})"
                        )

        return errors

    def validate_table(self, table_name: str, data: List[Dict[str, Any]],
                      all_tables_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Validate a table against its schema definition."""
        table_def = self.schema.get("tables", {}).get(table_name)
        if not table_def:
            return {
                "valid": False,
                "errors": [f"Table {table_name} not found in schema"],
                "warnings": []
            }

        errors = []
        warnings = []
        pk_field = table_def.get("primary_key")

        # Check for duplicates in PK
        if pk_field:
            pk_values = []
            for record in data:
                pk_value = record.get(pk_field)
                if pk_value is not None:
                    pk_values.append(pk_value)

            duplicates = [v for v in set(pk_values) if pk_values.count(v) > 1]
            if duplicates:
                errors.append(f"Duplicate primary keys found: {duplicates[:5]}")

        # Validate each record
        for i, record in enumerate(data):
            record_errors = self.validate_record(record, table_def, i)
            errors.extend(record_errors)
            self.stats["records_validated"] += 1

        # Validate foreign keys
        fk_errors = self.validate_foreign_keys(data, table_def, all_tables_data)
        errors.extend(fk_errors)

        # Check required fields at table level
        required_fields = [fname for fname, fdef in table_def.get("fields", {}).items()
                          if fdef.get("required", False)]
        for record in data:
            for req_field in required_fields:
                if req_field not in record or record[req_field] is None:
                    pk_value = record.get(pk_field, "unknown")
                    errors.append(f"Required field {req_field} missing (record PK: {pk_value})")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "record_count": len(data)
        }

    def load_data_file(self, file_path: Path) -> Optional[List[Dict[str, Any]]]:
        """Load data from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle different data structures
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # Check if data is wrapped with metadata
                if "data" in data:
                    return data["data"]
                else:
                    # Return as single record
                    return [data]
            else:
                return None
        except Exception as e:
            self.errors.append(f"Error loading {file_path}: {e}")
            return None

    def validate_file(self, file_path: Path, table_name: Optional[str] = None) -> Dict[str, Any]:
        """Validate a data file against schema."""
        self.stats["files_validated"] += 1

        data = self.load_data_file(file_path)
        if data is None:
            return {
                "valid": False,
                "errors": [f"Could not load data from {file_path}"],
                "warnings": []
            }

        # Determine table name if not provided
        if not table_name:
            # Try to infer from file path
            path_str = str(file_path)
            if "firms" in path_str or "firm" in path_str:
                table_name = "firms"
            elif "individual" in path_str:
                table_name = "individual_licenses"
            elif "connection" in path_str:
                table_name = "connections"
            elif "violation" in path_str:
                table_name = "violations"
            elif "evidence" in path_str:
                table_name = "evidence"
            else:
                return {
                    "valid": False,
                    "errors": [f"Could not determine table name for {file_path}"],
                    "warnings": []
                }

        # Load all tables for FK validation
        all_tables_data = self._load_all_tables()

        # Validate table
        result = self.validate_table(table_name, data, all_tables_data)
        result["file_path"] = str(file_path)
        result["table_name"] = table_name

        # Update stats
        if result["errors"]:
            self.stats["errors_found"] += len(result["errors"])
        if result["warnings"]:
            self.stats["warnings_found"] += len(result["warnings"])

        return result

    def _load_all_tables(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load all table data for FK validation."""
        tables_data = {}

        # Load firms
        firms_file = DATA_CLEANED_DIR / "firms.json"
        if firms_file.exists():
            data = self.load_data_file(firms_file)
            if data:
                tables_data["firms"] = data

        # Load individual licenses
        individual_file = DATA_CLEANED_DIR / "individual_licenses.json"
        if individual_file.exists():
            data = self.load_data_file(individual_file)
            if data:
                tables_data["individual_licenses"] = data

        # Load connections
        connections_file = RESEARCH_CONNECTIONS_DIR / "caitlin_skidmore_connections.json"
        if connections_file.exists():
            data = self.load_data_file(connections_file)
            if data:
                tables_data["connections"] = data

        return tables_data

    def generate_report(self) -> Dict[str, Any]:
        """Generate validation report."""
        return {
            "validation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "schema_version": self.schema.get("version", "unknown"),
            "statistics": self.stats,
            "errors": self.errors,
            "warnings": self.warnings
        }


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Validate data files against schema"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Specific file to validate"
    )
    parser.add_argument(
        "--table",
        type=str,
        help="Table name (if not inferrable from file path)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed validation output"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file for validation report (JSON)"
    )

    args = parser.parse_args()

    schema_path = PROJECT_ROOT / "data" / "schema.json"
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}")
        return 1

    validator = SchemaValidator(schema_path)

    if args.file:
        # Validate single file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            return 1

        result = validator.validate_file(file_path, args.table)

        if args.verbose:
            print(f"\nValidation Results for {file_path}")
            print(f"Table: {result.get('table_name', 'unknown')}")
            print(f"Records: {result.get('record_count', 0)}")
            print(f"Valid: {result['valid']}")

            if result["errors"]:
                print(f"\nErrors ({len(result['errors'])}):")
                for error in result["errors"][:10]:
                    print(f"  - {error}")
                if len(result["errors"]) > 10:
                    print(f"  ... and {len(result['errors']) - 10} more")

            if result["warnings"]:
                print(f"\nWarnings ({len(result['warnings'])}):")
                for warning in result["warnings"][:10]:
                    print(f"  - {warning}")
        else:
            status = "✓ VALID" if result["valid"] else "✗ INVALID"
            print(f"{status}: {file_path} ({result.get('record_count', 0)} records)")
            if result["errors"]:
                print(f"  Errors: {len(result['errors'])}")

        if args.output:
            report = validator.generate_report()
            report["file_results"] = [result]
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\nReport saved to {args.output}")

        return 0 if result["valid"] else 1
    else:
        # Validate all data files
        print("Validating all data files...")

        results = []

        # Validate firms
        firms_file = DATA_CLEANED_DIR / "firms.json"
        if firms_file.exists():
            result = validator.validate_file(firms_file, "firms")
            results.append(result)
            status = "✓" if result["valid"] else "✗"
            print(f"{status} {firms_file.name}: {result.get('record_count', 0)} records, "
                  f"{len(result['errors'])} errors")

        # Validate individual licenses
        individual_file = DATA_CLEANED_DIR / "individual_licenses.json"
        if individual_file.exists():
            result = validator.validate_file(individual_file, "individual_licenses")
            results.append(result)
            status = "✓" if result["valid"] else "✗"
            print(f"{status} {individual_file.name}: {result.get('record_count', 0)} records, "
                  f"{len(result['errors'])} errors")

        # Validate connections
        connections_file = RESEARCH_CONNECTIONS_DIR / "caitlin_skidmore_connections.json"
        if connections_file.exists():
            result = validator.validate_file(connections_file, "connections")
            results.append(result)
            status = "✓" if result["valid"] else "✗"
            print(f"{status} {connections_file.name}: {result.get('record_count', 0)} records, "
                  f"{len(result['errors'])} errors")

        # Generate report
        report = validator.generate_report()
        report["file_results"] = results

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\nReport saved to {args.output}")
        else:
            print(f"\nValidation Summary:")
            print(f"  Files validated: {validator.stats['files_validated']}")
            print(f"  Records validated: {validator.stats['records_validated']}")
            print(f"  Errors found: {validator.stats['errors_found']}")
            print(f"  Warnings found: {validator.stats['warnings_found']}")

        return 0 if validator.stats['errors_found'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
