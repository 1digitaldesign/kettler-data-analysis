#!/usr/bin/env python3
"""
Utility script to add metadata fields to JSON files.

This script adds standardized metadata fields (_metadata, _lineage, _validation)
to JSON files according to the metadata structure defined in data/metadata.json.

Usage:
    python scripts/utils/add_metadata.py <file_path> [--dry-run]
    python scripts/utils/add_metadata.py research/connections/*.json --dry-run
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import argparse

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_DIR, RESEARCH_DIR


def determine_file_category(file_path: Path) -> str:
    """Determine the category of a file based on its path."""
    path_str = str(file_path)

    if "connections" in path_str:
        return "connections"
    elif "violations" in path_str:
        return "violations"
    elif "anomalies" in path_str:
        return "anomalies"
    elif "evidence" in path_str:
        return "evidence"
    elif "verification" in path_str:
        return "verification"
    elif "timelines" in path_str:
        return "timelines"
    elif "summaries" in path_str:
        return "summaries"
    elif "search_results" in path_str or "search" in path_str:
        return "search_results"
    elif "va_dpor_complaint" in path_str:
        return "va_dpor_complaint"
    elif "analysis" in path_str:
        return "analysis"
    elif "cleaned" in path_str:
        return "cleaned_data"
    elif "source" in path_str:
        return "source_data"
    elif "vectors" in path_str:
        return "vectors"
    else:
        return "unknown"


def determine_source(file_path: Path, category: str) -> str:
    """Determine the source of a file."""
    if category == "source_data":
        if "firms" in str(file_path):
            return "Virginia DPOR"
        elif "individual" in str(file_path):
            return "Multi-State DPOR"
        else:
            return "Unknown"
    elif category == "cleaned_data":
        return "Data cleaning pipeline"
    elif category in ["connections", "violations", "anomalies", "analysis"]:
        return "Analysis pipeline"
    elif category == "evidence":
        return "Evidence extraction"
    elif category == "vectors":
        return "ETL pipeline"
    else:
        return "Research pipeline"


def determine_processing_script(file_path: Path, category: str) -> Optional[str]:
    """Determine the processing script for a file."""
    if category == "cleaned_data":
        return "bin/clean_data.py"
    elif category == "connections":
        return "bin/analyze_connections.py"
    elif category in ["violations", "anomalies", "analysis"]:
        return "scripts/core/unified_analysis.py"
    elif category == "evidence":
        return "bin/organize_evidence.py"
    elif category == "vectors":
        return "scripts/etl/etl_pipeline.py"
    elif category == "verification":
        return "bin/validate_data.py"
    else:
        return None


def determine_parent_files(file_path: Path, category: str) -> list:
    """Determine parent files for lineage tracking."""
    parents = []

    if category == "cleaned_data":
        if "firms" in str(file_path):
            parents.append("data/source/skidmore_all_firms_complete.json")
        elif "individual" in str(file_path):
            parents.append("data/source/skidmore_individual_licenses.json")
    elif category == "connections":
        parents.append("data/cleaned/firms.json")
        parents.append("data/cleaned/individual_licenses.json")
    elif category in ["violations", "anomalies"]:
        parents.append("research/connections/caitlin_skidmore_connections.json")
        parents.append("data/cleaned/firms.json")
    elif category == "evidence":
        # Try to find corresponding evidence files
        evidence_dir = PROJECT_ROOT / "evidence"
        if evidence_dir.exists():
            parents.append(f"evidence/{file_path.stem}.pdf")

    return parents


def add_metadata_to_file(file_path: Path, dry_run: bool = False) -> bool:
    """
    Add metadata fields to a JSON file.

    Args:
        file_path: Path to the JSON file
        dry_run: If True, don't write changes, just print what would be done

    Returns:
        True if successful, False otherwise
    """
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return False

    if file_path.suffix != ".json":
        print(f"Warning: Not a JSON file: {file_path}")
        return False

    # Read existing file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}")
        return False
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    # Determine file category and metadata
    category = determine_file_category(file_path)
    source = determine_source(file_path, category)
    processing_script = determine_processing_script(file_path, category)
    parent_files = determine_parent_files(file_path, category)

    # Check if metadata already exists
    has_metadata = "_metadata" in data or (isinstance(data, dict) and "_metadata" in data)

    if has_metadata and not dry_run:
        print(f"Info: {file_path} already has metadata, skipping")
        return True

    # Create metadata structure
    metadata = {
        "_metadata": {
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "source": source,
            "version": "1.0.0",
            "processing_script": processing_script,
            "description": f"{category.replace('_', ' ').title()} data file",
            "category": category
        },
        "_lineage": {
            "parent_files": parent_files,
            "transformation_steps": [],
            "dependencies": [processing_script] if processing_script else []
        },
        "_validation": {
            "validated": False,
            "validation_date": None,
            "validation_script": None,
            "issues": []
        }
    }

    # Add metadata to file
    if isinstance(data, dict):
        # If data is a dict, add metadata fields at the top level
        data.update(metadata)
        updated_data = data
    elif isinstance(data, list):
        # If data is a list, wrap it in a dict with metadata
        updated_data = {
            "_metadata": metadata["_metadata"],
            "_lineage": metadata["_lineage"],
            "_validation": metadata["_validation"],
            "data": data
        }
    else:
        print(f"Warning: Unexpected data type in {file_path}, skipping")
        return False

    # Write updated file
    if not dry_run:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=2, ensure_ascii=False)
            print(f"✓ Added metadata to {file_path}")
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False
    else:
        print(f"[DRY RUN] Would add metadata to {file_path}")
        print(f"  Category: {category}")
        print(f"  Source: {source}")
        print(f"  Processing script: {processing_script}")
        return True


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Add metadata fields to JSON files"
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="JSON files to process (supports glob patterns)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write changes, just print what would be done"
    )

    args = parser.parse_args()

    # Expand glob patterns
    import glob
    file_paths = []
    for pattern in args.files:
        file_paths.extend(glob.glob(pattern))

    if not file_paths:
        print("No files found matching patterns")
        return 1

    # Process each file
    success_count = 0
    for file_path_str in file_paths:
        file_path = Path(file_path_str)
        if add_metadata_to_file(file_path, dry_run=args.dry_run):
            success_count += 1

    print(f"\nProcessed {success_count}/{len(file_paths)} files")
    return 0 if success_count == len(file_paths) else 1


if __name__ == "__main__":
    sys.exit(main())
