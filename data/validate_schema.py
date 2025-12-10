#!/usr/bin/env python3
"""
Schema Validation Script

Validates all data files against the schema definition in schema.json.
Ensures data integrity, primary key uniqueness, and foreign key relationships.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

class SchemaValidator:
    def __init__(self, schema_path: str = "schema.json"):
        """Initialize validator with schema definition."""
        self.schema_path = Path(schema_path)
        self.data_dir = self.schema_path.parent
        with open(self.schema_path, 'r') as f:
            self.schema = json.load(f)
        self.errors = []
        self.warnings = []

    def validate_all(self) -> bool:
        """Validate all tables against schema."""
        print("=" * 70)
        print("SCHEMA VALIDATION REPORT")
        print("=" * 70)
        print(f"Schema: {self.schema_path}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Validate each table
        for table_name, table_def in self.schema['tables'].items():
            print(f"\n{'='*70}")
            print(f"Validating Table: {table_name}")
            print(f"{'='*70}")
            self.validate_table(table_name, table_def)

        # Validate relationships
        print(f"\n{'='*70}")
        print("Validating Relationships")
        print(f"{'='*70}")
        self.validate_relationships()

        # Print summary
        self.print_summary()

        return len(self.errors) == 0

    def validate_table(self, table_name: str, table_def: Dict[str, Any]):
        """Validate a single table."""
        # Handle both 'file' and 'files' keys
        if 'file' in table_def:
            file_paths = [table_def['file']]
        elif 'files' in table_def:
            file_paths = table_def['files']
        else:
            self.warnings.append(f"{table_name}: No file(s) specified in schema")
            print(f"⚠️  No file(s) specified for {table_name}")
            return

        # Validate each file
        all_data = []
        for file_path_str in file_paths:
            file_path = self.data_dir / file_path_str

            if not file_path.exists():
                self.warnings.append(f"{table_name}: File not found: {file_path}")
                print(f"⚠️  File not found: {file_path}")
                continue

            # Load data
            data = self.load_data(file_path, table_name)
            if data:
                all_data.extend(data)

        if not all_data:
            return

        data = all_data

        # Get primary key
        pk = table_def['primary_key']

        # Validate primary key uniqueness (skip if PK is computed/generated)
        if not table_def.get('columns', {}).get(pk, {}).get('computed', False):
            self.validate_primary_key(table_name, data, pk, table_def)

        # Validate columns
        self.validate_columns(table_name, data, table_def)

        # Validate constraints
        self.validate_constraints(table_name, data, table_def)

        # Validate data quality rules
        self.validate_data_quality(table_name, data, table_def)

    def load_data(self, file_path: Path, table_name: str) -> Optional[List[Dict]]:
        """Load data from file."""
        try:
            with open(file_path, 'r') as f:
                if file_path.suffix == '.json':
                    data = json.load(f)
                    # Handle nested structure (e.g., {"companies": [...]})
                    if isinstance(data, dict) and 'companies' in data:
                        return data['companies']
                    elif isinstance(data, dict) and 'listings' in data:
                        return data['listings']
                    elif isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and table_name == 'analysis_results':
                        # Analysis results are single objects, add filename and wrap in list
                        data_with_filename = data.copy()
                        data_with_filename['file_name'] = str(file_path.name)
                        return [data_with_filename]
                    else:
                        self.warnings.append(f"{table_name}: Unexpected JSON structure - treating as single record")
                        return [data] if isinstance(data, dict) else None
                elif file_path.suffix == '.csv':
                    import csv
                    reader = csv.DictReader(f)
                    return list(reader)
        except Exception as e:
            self.errors.append(f"{table_name}: Error loading file: {e}")
            print(f"❌ Error loading {file_path}: {e}")
            return None

    def validate_primary_key(self, table_name: str, data: List[Dict], pk: str, table_def: Dict):
        """Validate primary key uniqueness."""
        pk_values = []
        null_pks = []

        for i, record in enumerate(data):
            pk_value = record.get(pk)
            if pk_value is None or pk_value == '':
                null_pks.append(i + 1)
            else:
                pk_values.append(pk_value)

        # Check for null primary keys
        if null_pks:
            self.errors.append(f"{table_name}: NULL primary keys found at rows: {null_pks}")
            print(f"❌ NULL primary keys found at rows: {null_pks}")

        # Check for duplicates
        duplicates = self.find_duplicates(pk_values)
        if duplicates:
            self.errors.append(f"{table_name}: Duplicate primary keys: {duplicates}")
            print(f"❌ Duplicate primary keys found: {len(duplicates)} duplicates")
            for dup_value, count in duplicates.items():
                print(f"   - {pk}={dup_value}: {count} occurrences")
        else:
            print(f"✅ Primary key '{pk}' is unique ({len(pk_values)} records)")

    def validate_columns(self, table_name: str, data: List[Dict], table_def: Dict):
        """Validate column types and required fields."""
        columns = table_def['columns']
        required_cols = [col for col, defn in columns.items() if defn.get('required', False)]

        for i, record in enumerate(data):
            # Check required columns (skip if column is computed)
            for col in required_cols:
                col_def = columns.get(col, {})
                if col_def.get('computed', False):
                    continue  # Skip computed columns
                if col not in record or record[col] is None or record[col] == '':
                    self.errors.append(f"{table_name}: Row {i+1}: Missing required column '{col}'")

            # Validate column types and formats
            for col, defn in columns.items():
                if col not in record:
                    continue

                value = record[col]
                if value is None or value == '':
                    continue

                # Validate format patterns
                if 'pattern' in defn:
                    pattern = defn['pattern']
                    if not re.match(pattern, str(value)):
                        self.errors.append(
                            f"{table_name}: Row {i+1}: Column '{col}'='{value}' "
                            f"does not match pattern '{pattern}'"
                        )

                # Validate enums
                if 'enum' in defn:
                    if value not in defn['enum']:
                        self.errors.append(
                            f"{table_name}: Row {i+1}: Column '{col}'='{value}' "
                            f"not in enum {defn['enum']}"
                        )

        print(f"✅ Column validation complete ({len(columns)} columns checked)")

    def validate_constraints(self, table_name: str, data: List[Dict], table_def: Dict):
        """Validate table constraints."""
        constraints = self.schema.get('constraints', [])
        table_constraints = [c for c in constraints if c.get('table') == table_name]

        for constraint in table_constraints:
            constraint_name = constraint['name']
            condition = constraint['condition']

            # Simple constraint validation (can be extended)
            if 'principal_broker' in condition:
                for i, record in enumerate(data):
                    if record.get('principal_broker') != 'SKIDMORE CAITLIN MARIE':
                        self.errors.append(
                            f"{table_name}: Row {i+1}: Constraint '{constraint_name}' violated"
                        )

            if 'expiration_date' in condition and 'initial_cert_date' in condition:
                for i, record in enumerate(data):
                    exp_date = record.get('expiration_date')
                    init_date = record.get('initial_cert_date')
                    if exp_date and init_date:
                        if datetime.fromisoformat(exp_date) <= datetime.fromisoformat(init_date):
                            self.errors.append(
                                f"{table_name}: Row {i+1}: expiration_date must be after initial_cert_date"
                            )

        if table_constraints:
            print(f"✅ Constraint validation complete ({len(table_constraints)} constraints)")

    def validate_data_quality(self, table_name: str, data: List[Dict], table_def: Dict):
        """Validate data quality rules."""
        rules = self.schema.get('data_quality_rules', [])
        table_rules = [r for r in rules if r.get('table') == table_name]

        for rule in table_rules:
            validation = rule['validation']

            if 'regex_match' in validation:
                # Extract pattern and column
                match = re.search(r"regex_match\((\w+),\s*'([^']+)'\)", validation)
                if match:
                    col_name = match.group(1)
                    pattern = match.group(2)
                    for i, record in enumerate(data):
                        value = record.get(col_name)
                        if value and not re.match(pattern, str(value)):
                            self.errors.append(
                                f"{table_name}: Row {i+1}: {rule['rule']} - "
                                f"'{col_name}'='{value}' does not match pattern"
                            )

            if 'IS NOT NULL' in validation:
                # Extract column name from validation string
                # Format: "column_name IS NOT NULL"
                parts = validation.split('IS NOT NULL')[0].strip()
                col_name = parts.split()[-1] if parts else None
                if col_name:
                    for i, record in enumerate(data):
                        if record.get(col_name) is None or record.get(col_name) == '':
                            self.errors.append(
                                f"{table_name}: Row {i+1}: {rule['rule']} - '{col_name}' is NULL"
                            )

        if table_rules:
            print(f"✅ Data quality validation complete ({len(table_rules)} rules)")

    def validate_relationships(self):
        """Validate foreign key relationships."""
        relationships = self.schema.get('relationships', [])

        # Load referenced tables
        referenced_tables = {}
        for rel in relationships:
            to_table = rel['to_table']
            if to_table not in referenced_tables:
                table_def = self.schema['tables'][to_table]
                # Handle both 'file' and 'files' keys
                if 'file' in table_def:
                    file_paths = [table_def['file']]
                elif 'files' in table_def:
                    file_paths = table_def['files']
                else:
                    continue

                all_data = []
                for file_path_str in file_paths:
                    file_path = self.data_dir / file_path_str
                    if file_path.exists():
                        data = self.load_data(file_path, to_table)
                        if data:
                            all_data.extend(data)
                referenced_tables[to_table] = all_data

        # Validate each relationship
        for rel in relationships:
            from_table = rel['from_table']
            from_col = rel['from_column']
            to_table = rel['to_table']
            to_col = rel['to_column']

            # Load source table
            from_table_def = self.schema['tables'][from_table]
            # Handle both 'file' and 'files' keys
            if 'file' in from_table_def:
                file_paths = [from_table_def['file']]
            elif 'files' in from_table_def:
                file_paths = from_table_def['files']
            else:
                continue

            all_from_data = []
            for file_path_str in file_paths:
                file_path = self.data_dir / file_path_str
                if file_path.exists():
                    data = self.load_data(file_path, from_table)
                    if data:
                        all_from_data.extend(data)
            from_data = all_from_data

            if from_data is None:
                continue

            # Get valid foreign key values
            valid_fk_values = set()
            for record in referenced_tables.get(to_table, []):
                fk_value = record.get(to_col)
                if fk_value:
                    valid_fk_values.add(str(fk_value))

            # Check foreign key references
            invalid_refs = []
            for i, record in enumerate(from_data):
                fk_value = record.get(from_col)
                if fk_value and str(fk_value) != 'null' and str(fk_value) != '':
                    fk_str = str(fk_value)
                    # Try exact match first
                    if fk_str not in valid_fk_values:
                        # Try zero-padded version (for 9-digit license numbers)
                        if len(fk_str) == 9:
                            padded = '0' + fk_str
                            if padded in valid_fk_values:
                                continue  # Valid after padding
                        # Try without leading zero
                        if fk_str.startswith('0') and len(fk_str) == 10:
                            unpadded = fk_str[1:]
                            if unpadded in valid_fk_values:
                                continue  # Valid without leading zero
                        invalid_refs.append((i+1, fk_value))

            if invalid_refs:
                self.errors.append(
                    f"{from_table}.{from_col} → {to_table}.{to_col}: "
                    f"{len(invalid_refs)} invalid foreign key references"
                )
                print(f"❌ Invalid FK references: {len(invalid_refs)}")
                for row, value in invalid_refs[:5]:  # Show first 5
                    print(f"   - Row {row}: {from_col}={value} not found in {to_table}")
            else:
                print(f"✅ FK {from_table}.{from_col} → {to_table}.{to_col}: Valid")

    def find_duplicates(self, values: List[Any]) -> Dict[Any, int]:
        """Find duplicate values."""
        counts = defaultdict(int)
        for value in values:
            counts[value] += 1
        return {value: count for value, count in counts.items() if count > 1}

    def print_summary(self):
        """Print validation summary."""
        print(f"\n{'='*70}")
        print("VALIDATION SUMMARY")
        print(f"{'='*70}")
        print(f"Errors:   {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")

        if self.errors:
            print(f"\n❌ ERRORS FOUND:")
            for error in self.errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more errors")

        if self.warnings:
            print(f"\n⚠️  WARNINGS:")
            for warning in self.warnings[:5]:  # Show first 5 warnings
                print(f"  - {warning}")
            if len(self.warnings) > 5:
                print(f"  ... and {len(self.warnings) - 5} more warnings")

        if not self.errors and not self.warnings:
            print("\n✅ All validations passed!")
        elif not self.errors:
            print("\n⚠️  Validation completed with warnings")
        else:
            print("\n❌ Validation failed")


def main():
    """Run schema validation."""
    validator = SchemaValidator()
    success = validator.validate_all()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
