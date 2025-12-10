#!/usr/bin/env python3
"""
Utility script to add metadata fields to JSON files.

This script adds standardized metadata fields (_metadata, _lineage, _validation)
to JSON files according to the metadata structure defined in data/metadata.json.

Uses Python 3.14 features: modern type hints, except expressions, efficient patterns.

Usage:
    python scripts/utils/add_metadata.py <file_path> [--dry-run]
    python scripts/utils/add_metadata.py research/connections/*.json --dry-run
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Optional
import argparse
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_DIR, RESEARCH_DIR


def determine_file_category(file_path: Path) -> str:
    """Determine the category of a file based on its path using match expression."""
    path_str = str(file_path).lower()

    match path_str:
        case p if "connections" in p:
            return "connections"
        case p if "violations" in p:
            return "violations"
        case p if "anomalies" in p:
            return "anomalies"
        case p if "evidence" in p:
            return "evidence"
        case p if "verification" in p:
            return "verification"
        case p if "timelines" in p:
            return "timelines"
        case p if "summaries" in p:
            return "summaries"
        case p if "search_results" in p or "search" in p:
            return "search_results"
        case p if "va_dpor_complaint" in p:
            return "va_dpor_complaint"
        case p if "analysis" in p:
            return "analysis"
        case p if "cleaned" in p:
            return "cleaned_data"
        case p if "source" in p:
            return "source_data"
        case p if "vectors" in p:
            return "vectors"
        case _:
            return "unknown"


def determine_source(file_path: Path, category: str) -> str:
    """Determine the source of a file."""
    match category:
        case "source_data":
            return "Virginia DPOR" if "firms" in str(file_path) else "Multi-State DPOR" if "individual" in str(file_path) else "Unknown"
        case "cleaned_data":
            return "Data cleaning pipeline"
        case cat if cat in ["connections", "violations", "anomalies", "analysis"]:
            return "Analysis pipeline"
        case "evidence":
            return "Evidence extraction"
        case "vectors":
            return "ETL pipeline"
        case _:
            return "Research pipeline"


def determine_processing_script(file_path: Path, category: str) -> Optional[str]:
    """Determine the processing script for a file."""
    script_map = {
        "cleaned_data": "bin/clean_data.py",
        "connections": "bin/analyze_connections.py",
        "violations": "scripts/core/unified_analysis.py",
        "anomalies": "scripts/core/unified_analysis.py",
        "analysis": "scripts/core/unified_analysis.py",
        "evidence": "bin/organize_evidence.py",
        "vectors": "scripts/etl/etl_pipeline.py",
        "verification": "bin/validate_data.py",
    }
    return script_map.get(category)


def determine_parent_files(file_path: Path, category: str) -> list[str]:
    """Determine parent files for lineage tracking."""
    parents = []

    match category:
        case "cleaned_data":
            if "firms" in str(file_path):
                parents.append("data/source/skidmore_all_firms_complete.json")
            elif "individual" in str(file_path):
                parents.append("data/source/skidmore_individual_licenses.json")
        case "connections":
            parents.extend([
                "data/cleaned/firms.json",
                "data/cleaned/individual_licenses.json"
            ])
        case cat if cat in ["violations", "anomalies"]:
            parents.extend([
                "research/connections/caitlin_skidmore_connections.json",
                "data/cleaned/firms.json"
            ])
        case "evidence":
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

    # Read existing file using except expression (PEP 758)
    try:
        data = json.loads(file_path.read_text(encoding='utf-8'))
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
    has_metadata = "_metadata" in data if isinstance(data, dict) else False

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
    match data:
        case dict():
            updated_data = data | metadata  # Python 3.14: dict union operator
        case list():
            updated_data = {
                "_metadata": metadata["_metadata"],
                "_lineage": metadata["_lineage"],
                "_validation": metadata["_validation"],
                "data": data
            }
        case _:
            print(f"Warning: Unexpected data type in {file_path}, skipping")
            return False

    # Write updated file
    if not dry_run:
        try:
            file_path.write_text(
                json.dumps(updated_data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
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


def main() -> int:
    """Main function."""
    parser = argparse.ArgumentParser(description="Add metadata fields to JSON files")
    parser.add_argument("files", nargs="+", help="JSON files to process (supports glob patterns)")
    parser.add_argument("--dry-run", action="store_true", help="Don't write changes, just print what would be done")

    args = parser.parse_args()

    # Expand glob patterns
    from glob import glob
    file_paths = [Path(f) for pattern in args.files for f in glob(pattern)]

    if not file_paths:
        print("No files found matching patterns")
        return 1

    # Process each file
    success_count = sum(
        1 for file_path in file_paths
        if add_metadata_to_file(file_path, dry_run=args.dry_run)
    )

    print(f"\nProcessed {success_count}/{len(file_paths)} files")
    return 0 if success_count == len(file_paths) else 1


if __name__ == "__main__":
    sys.exit(main())
