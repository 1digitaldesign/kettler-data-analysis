#!/usr/bin/env python3
"""
Parallel Data Cleaning and Normalization Script

Leverages ARM M4 MAX architecture with multiprocessing for efficient parallel processing.
Normalizes state/jurisdiction names across all JSON files in the project.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp
from datetime import datetime
import traceback

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.state_normalizer import (
    normalize_state,
    normalize_dict_recursive,
    find_state_fields,
    STATE_NORMALIZATION_MAP
)
from scripts.utils.paths import PROJECT_ROOT


def get_cpu_count() -> int:
    """
    Get optimal number of worker processes for ARM M4 MAX.
    Uses all available CPU cores for maximum parallelism.
    """
    # ARM M4 MAX typically has 12-16 performance cores
    # Use all available cores minus 1 for system overhead
    cpu_count = mp.cpu_count()
    # Use 80% of available cores to leave headroom
    optimal_workers = max(1, int(cpu_count * 0.8))
    return optimal_workers


def normalize_json_file(file_path: Path) -> Tuple[str, Dict[str, Any]]:
    """
    Normalize a single JSON file.

    Args:
        file_path: Path to JSON file to normalize

    Returns:
        Tuple of (file_path_str, result_dict) where result_dict contains:
        - success: bool
        - changes: int (number of changes made)
        - fields_found: List[str] (paths to state fields found)
        - error: Optional[str]
    """
    result = {
        "success": False,
        "changes": 0,
        "fields_found": [],
        "error": None,
        "file_size": 0
    }

    try:
        file_path_str = str(file_path)
        result["file_size"] = file_path.stat().st_size

        # Skip very large files that might cause memory issues (>100MB)
        if result["file_size"] > 100 * 1024 * 1024:
            result["error"] = "File too large (>100MB), skipping"
            return (file_path_str, result)

        # Read JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Find state fields before normalization
        fields_before = find_state_fields(data)
        result["fields_found"] = fields_before

        # Normalize the data
        normalized_data = normalize_dict_recursive(data)

        # Count changes by comparing serialized JSON (simple heuristic)
        original_json = json.dumps(data, sort_keys=True)
        normalized_json = json.dumps(normalized_data, sort_keys=True)

        if original_json != normalized_json:
            # Write normalized data back
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(normalized_data, f, indent=2, ensure_ascii=False)

            # Estimate changes (rough count of differences)
            result["changes"] = len(fields_before)
            result["success"] = True
        else:
            result["success"] = True
            result["changes"] = 0

    except json.JSONDecodeError as e:
        result["error"] = f"JSON decode error: {str(e)}"
    except Exception as e:
        result["error"] = f"Error: {str(e)}\n{traceback.format_exc()}"

    return (file_path_str, result)


def find_all_json_files(root_dir: Path, exclude_patterns: List[str] = None) -> List[Path]:
    """
    Find all JSON files in the project, excluding certain patterns.

    Args:
        root_dir: Root directory to search
        exclude_patterns: List of patterns to exclude (e.g., ['node_modules', '.git'])

    Returns:
        List of Path objects for JSON files
    """
    if exclude_patterns is None:
        exclude_patterns = ['node_modules', '.git', '__pycache__', '.venv', 'venv', '.cursor']

    json_files = []
    for json_file in root_dir.rglob('*.json'):
        # Skip excluded patterns
        if any(pattern in str(json_file) for pattern in exclude_patterns):
            continue

        # Skip if file is too large (>100MB)
        try:
            if json_file.stat().st_size > 100 * 1024 * 1024:
                continue
        except (OSError, FileNotFoundError):
            continue

        json_files.append(json_file)

    return json_files


def process_files_parallel(
    json_files: List[Path],
    max_workers: Optional[int] = None,
    progress_callback: Optional[callable] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Process JSON files in parallel using multiprocessing.

    Args:
        json_files: List of JSON file paths to process
        max_workers: Maximum number of worker processes (None = auto-detect)
        progress_callback: Optional callback function for progress updates

    Returns:
        Dictionary mapping file paths to result dictionaries
    """
    if max_workers is None:
        max_workers = get_cpu_count()

    results = {}
    total_files = len(json_files)
    processed = 0

    print(f"Processing {total_files} JSON files with {max_workers} worker processes...")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(normalize_json_file, file_path): file_path
            for file_path in json_files
        }

        # Process completed tasks
        for future in as_completed(future_to_file):
            file_path_str, result = future.result()
            results[file_path_str] = result
            processed += 1

            if progress_callback:
                progress_callback(processed, total_files, file_path_str, result)
            else:
                status = "✓" if result["success"] else "✗"
                changes = result["changes"]
                print(f"  [{processed}/{total_files}] {status} {Path(file_path_str).name} ({changes} changes)")

    return results


def generate_summary_report(results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a summary report from processing results.

    Args:
        results: Dictionary of file paths to result dictionaries

    Returns:
        Summary dictionary with statistics
    """
    total_files = len(results)
    successful = sum(1 for r in results.values() if r["success"])
    failed = total_files - successful
    total_changes = sum(r["changes"] for r in results.values())
    total_size = sum(r.get("file_size", 0) for r in results.values())

    errors = [r["error"] for r in results.values() if r.get("error")]

    # Files with most changes
    files_with_changes = [
        (path, r["changes"]) for path, r in results.items() if r["changes"] > 0
    ]
    files_with_changes.sort(key=lambda x: x[1], reverse=True)

    return {
        "total_files": total_files,
        "successful": successful,
        "failed": failed,
        "total_changes": total_changes,
        "total_size_mb": total_size / (1024 * 1024),
        "errors": errors,
        "top_changed_files": files_with_changes[:10],
        "timestamp": datetime.now().isoformat()
    }


def main():
    """Main entry point for parallel data cleaning."""
    print("=" * 80)
    print("Parallel Data Cleaning and Normalization")
    print("=" * 80)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"CPU Cores Available: {mp.cpu_count()}")
    print(f"Optimal Workers: {get_cpu_count()}")
    print("=" * 80)
    print()

    # Find all JSON files
    print("Scanning for JSON files...")
    json_files = find_all_json_files(PROJECT_ROOT)
    print(f"Found {len(json_files)} JSON files to process")
    print()

    if not json_files:
        print("No JSON files found. Exiting.")
        return

    # Process files in parallel
    results = process_files_parallel(json_files)

    # Generate summary
    print()
    print("=" * 80)
    print("Processing Summary")
    print("=" * 80)
    summary = generate_summary_report(results)

    print(f"Total Files: {summary['total_files']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Total Changes: {summary['total_changes']}")
    print(f"Total Size Processed: {summary['total_size_mb']:.2f} MB")
    print()

    if summary['top_changed_files']:
        print("Top 10 Files with Changes:")
        for path, changes in summary['top_changed_files']:
            print(f"  {changes:4d} changes: {Path(path).name}")
        print()

    if summary['errors']:
        print(f"Errors ({len(summary['errors'])}):")
        for error in summary['errors'][:10]:  # Show first 10 errors
            print(f"  - {error}")
        print()

    # Save summary report
    summary_file = PROJECT_ROOT / "data" / "processed" / "normalization_summary.json"
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            "summary": summary,
            "all_results": results
        }, f, indent=2, ensure_ascii=False)

    print(f"Summary report saved to: {summary_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
