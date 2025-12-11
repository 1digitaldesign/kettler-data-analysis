#!/usr/bin/env python3
"""
Validation Script for State/Jurisdiction Normalization

Validates that all state/jurisdiction references are normalized consistently.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_DIR, RESEARCH_DIR
from scripts.utils.state_normalizer import STATE_NORMALIZATION_MAP, normalize_state


def find_unnormalized_keys(data: Any, path: str = "", issues: List[Dict] = None) -> List[Dict]:
    """
    Find dictionary keys that should be normalized.

    Args:
        data: Data structure to check
        path: Current path in structure
        issues: List of issues found

    Returns:
        List of issues found
    """
    if issues is None:
        issues = []

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key

            # Check if key is a state identifier that needs normalization
            if isinstance(key, str):
                normalized_key = normalize_state(key)
                if normalized_key != key and normalized_key in STATE_NORMALIZATION_MAP.values():
                    issues.append({
                        "type": "unnormalized_key",
                        "path": current_path,
                        "current": key,
                        "should_be": normalized_key,
                        "value_preview": str(value)[:100] if not isinstance(value, (dict, list)) else type(value).__name__
                    })

            # Recurse
            find_unnormalized_keys(value, current_path, issues)

    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]" if path else f"[{i}]"
            find_unnormalized_keys(item, current_path, issues)

    return issues


def validate_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Validate a single JSON file for normalization issues.

    Args:
        file_path: Path to JSON file

    Returns:
        Dictionary with validation results
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        issues = find_unnormalized_keys(data)

        return {
            "file": str(file_path),
            "valid": len(issues) == 0,
            "issues": issues,
            "issue_count": len(issues)
        }

    except json.JSONDecodeError as e:
        return {
            "file": str(file_path),
            "valid": False,
            "issues": [{"type": "json_error", "error": str(e)}],
            "issue_count": 1
        }
    except Exception as e:
        return {
            "file": str(file_path),
            "valid": False,
            "issues": [{"type": "error", "error": str(e)}],
            "issue_count": 1
        }


def validate_all_files() -> Dict[str, Any]:
    """
    Validate all JSON files for normalization consistency.

    Returns:
        Dictionary with validation results
    """
    results = {
        "total_files": 0,
        "valid_files": 0,
        "invalid_files": 0,
        "total_issues": 0,
        "issues_by_type": defaultdict(int),
        "files_with_issues": []
    }

    # Find JSON files
    json_files = []
    for search_dir in [DATA_DIR, RESEARCH_DIR, PROJECT_ROOT / "ref"]:
        if search_dir.exists():
            json_files.extend(search_dir.rglob('*.json'))

    json_files = list(set(json_files))
    results["total_files"] = len(json_files)

    print(f"Validating {len(json_files)} JSON files...\n")

    for json_file in json_files:
        # Skip very large files
        try:
            if json_file.stat().st_size > 100 * 1024 * 1024:
                continue
        except OSError:
            continue

        validation = validate_json_file(json_file)

        if validation["valid"]:
            results["valid_files"] += 1
        else:
            results["invalid_files"] += 1
            results["total_issues"] += validation["issue_count"]

            for issue in validation["issues"]:
                results["issues_by_type"][issue["type"]] += 1

            if validation["issue_count"] > 0:
                results["files_with_issues"].append(validation)

    return results


def main():
    """Main execution function."""
    print("=" * 80)
    print("State/Jurisdiction Normalization Validation")
    print("=" * 80)
    print()

    results = validate_all_files()

    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total files checked: {results['total_files']}")
    print(f"Valid files: {results['valid_files']}")
    print(f"Files with issues: {results['invalid_files']}")
    print(f"Total issues found: {results['total_issues']}")
    print()

    if results['issues_by_type']:
        print("Issues by type:")
        for issue_type, count in sorted(results['issues_by_type'].items()):
            print(f"  {issue_type}: {count}")
        print()

    if results['files_with_issues']:
        print("Files with issues (showing first 10):")
        for file_result in results['files_with_issues'][:10]:
            print(f"  {file_result['file']}: {file_result['issue_count']} issues")
            for issue in file_result['issues'][:3]:  # Show first 3 issues per file
                if issue['type'] == 'unnormalized_key':
                    print(f"    - Key '{issue['current']}' should be '{issue['should_be']}' at {issue['path']}")

        if len(results['files_with_issues']) > 10:
            print(f"  ... and {len(results['files_with_issues']) - 10} more files with issues")

    print()
    print("=" * 80)

    if results['total_issues'] == 0:
        print("✓ All files are properly normalized!")
    else:
        print(f"⚠ Found {results['total_issues']} normalization issues")

    print("=" * 80)


if __name__ == "__main__":
    main()
