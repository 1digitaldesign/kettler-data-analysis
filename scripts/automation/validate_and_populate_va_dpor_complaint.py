#!/usr/bin/env python3
"""
Validate, clean, and populate va_dpor_complaint JSON files.
Ensures all files have complete metadata and proper structure.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

PROJECT_ROOT = Path(__file__).parent.parent.parent
VA_DPOR_DIR = PROJECT_ROOT / "research" / "va_dpor_complaint"

def ensure_metadata(data: Dict[str, Any], file_path: Path) -> Dict[str, Any]:
    """Ensure metadata section is complete"""
    # Check if metadata exists at root level
    if "metadata" not in data and "_metadata" not in data:
        data["metadata"] = {}

    metadata = data.get("metadata") or data.get("_metadata", {})

    # Add standard metadata fields if missing
    if "file_name" not in metadata:
        metadata["file_name"] = file_path.name

    if "file_path" not in metadata:
        metadata["file_path"] = str(file_path.relative_to(PROJECT_ROOT))

    if "last_updated" not in metadata:
        metadata["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "source" not in metadata:
        metadata["source"] = "Kettler Data Analysis Project - VA DPOR Complaint Research"

    if "status" not in metadata:
        metadata["status"] = "complete"

    # Ensure metadata is at root level
    if "_metadata" in data:
        data["metadata"] = metadata
        del data["_metadata"]
    else:
        data["metadata"] = metadata

    return data

def clean_null_values(obj: Any, context: str = "") -> Any:
    """Clean null values - preserve nulls for dates/unknowns, replace others"""
    if obj is None:
        if "date" in context.lower() and "unknown" not in context.lower():
            return None  # Keep null for unknown dates
        elif "url" in context.lower():
            return ""
        elif "email" in context.lower():
            return ""
        elif "phone" in context.lower():
            return ""
        elif "address" in context.lower():
            return ""
        elif "name" in context.lower():
            return ""
        elif "note" in context.lower() or "description" in context.lower():
            return "No information available"
        elif "status" in context.lower():
            return "unknown"
        elif "count" in context.lower() or "number" in context.lower():
            return 0
        else:
            return None  # Preserve null for truly unknown data
    elif isinstance(obj, dict):
        return {k: clean_null_values(v, k) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_null_values(item, context) for item in obj]
    else:
        return obj

def validate_structure(data: Dict[str, Any], file_path: Path) -> List[str]:
    """Validate file structure and return list of issues"""
    issues = []

    # Check for required fields based on file type
    filename = file_path.name.lower()

    if "gap" in filename or "operations" in filename:
        if "gap_period" not in data and "research_date" not in data:
            issues.append("Missing gap_period or research_date")

    if "violation" in filename or "rule" in filename:
        if "violation_analysis" not in data and "regulation" not in data:
            issues.append("Missing violation_analysis or regulation")

    if "personnel" in filename or "verification" in filename:
        if "personnel" not in data and "verification" not in data:
            issues.append("Missing personnel or verification data")

    return issues

def validate_and_clean_file(file_path: Path) -> tuple[bool, List[str]]:
    """Validate and clean a single JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        original = json.dumps(data, sort_keys=True)
        issues = []

        # Ensure metadata
        data = ensure_metadata(data, file_path)

        # Clean null values
        data = clean_null_values(data)

        # Validate structure
        struct_issues = validate_structure(data, file_path)
        issues.extend(struct_issues)

        # Check if changed
        new_data = json.dumps(data, sort_keys=True)
        if original != new_data:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True, issues

        return False, issues

    except Exception as e:
        return False, [f"Error: {str(e)}"]

def validate_all_files():
    """Validate and clean all JSON files in va_dpor_complaint directory"""
    json_files = list(VA_DPOR_DIR.glob("*.json"))

    print(f"Found {len(json_files)} JSON files to validate and clean")
    print()

    updated_count = 0
    issues_found = []

    for file_path in sorted(json_files):
        updated, issues = validate_and_clean_file(file_path)

        if updated:
            updated_count += 1
            print(f"  ✓ Updated {file_path.name}")
        else:
            print(f"  - {file_path.name}")

        if issues:
            issues_found.append((file_path.name, issues))
            for issue in issues:
                print(f"    ⚠ {issue}")

    print()
    print(f"{'='*60}")
    print(f"Validation complete:")
    print(f"  ✓ {updated_count} files updated")
    print(f"  - {len(json_files) - updated_count} files already clean")
    if issues_found:
        print(f"  ⚠ {len(issues_found)} files have structural issues")

    return issues_found

if __name__ == "__main__":
    validate_all_files()
