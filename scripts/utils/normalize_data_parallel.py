#!/usr/bin/env python3
"""
Parallel Data Normalization Script

Uses multiprocessing to leverage ARM M4 MAX virtual threads for efficient
parallel processing of JSON files to normalize state/jurisdiction references.

Optimized for ARM M4 MAX architecture with maximum parallelization.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import time
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_DIR, RESEARCH_DIR
REF_DIR = PROJECT_ROOT / "ref"
from scripts.utils.state_normalizer import (
    normalize_state,
    normalize_jurisdiction,
    normalize_dict_recursive,
    STATE_NORMALIZATION_MAP
)


def get_optimal_worker_count() -> int:
    """
    Get optimal worker count for ARM M4 MAX.
    Uses all available CPU cores for maximum parallelization.
    """
    # ARM M4 MAX typically has many performance cores
    # Use all available cores for maximum throughput
    available_cores = cpu_count()

    # For I/O-bound tasks (JSON file reading/writing), we can use more workers
    # than CPU cores. For CPU-bound tasks, use CPU count.
    # Since we're doing both I/O and CPU work, use a multiplier
    optimal_workers = min(available_cores * 2, 32)  # Cap at 32 to avoid overhead

    print(f"Detected {available_cores} CPU cores")
    print(f"Using {optimal_workers} worker processes for parallel processing")

    return optimal_workers


def find_json_files(root_dir: Path, exclude_patterns: List[str] = None) -> List[Path]:
    """
    Find all JSON files in the directory tree.

    Args:
        root_dir: Root directory to search
        exclude_patterns: List of patterns to exclude (e.g., ['node_modules', '.git'])

    Returns:
        List of JSON file paths
    """
    if exclude_patterns is None:
        exclude_patterns = ['.git', 'node_modules', '__pycache__', '.venv', 'venv']

    json_files = []

    for json_file in root_dir.rglob('*.json'):
        # Skip excluded patterns
        if any(pattern in str(json_file) for pattern in exclude_patterns):
            continue

        # Skip very large files that might cause memory issues
        try:
            file_size = json_file.stat().st_size
            # Skip files larger than 100MB
            if file_size > 100 * 1024 * 1024:
                print(f"Skipping large file: {json_file} ({file_size / 1024 / 1024:.1f} MB)")
                continue
        except OSError:
            continue

        json_files.append(json_file)

    return sorted(json_files)


def normalize_json_file(file_path: Path) -> Tuple[Path, bool, str, int]:
    """
    Normalize a single JSON file.

    Args:
        file_path: Path to JSON file to normalize

    Returns:
        Tuple of (file_path, success, message, changes_count)
    """
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Track original for comparison
        original_data = json.dumps(data, sort_keys=True)

        # Normalize the data
        normalized_data = normalize_dict_recursive(data)

        # Check if changes were made
        normalized_json = json.dumps(normalized_data, sort_keys=True)
        changes_made = original_data != normalized_json

        if changes_made:
            # Count approximate changes (rough estimate)
            changes_count = (original_data.count('district_of_columbia') +
                          original_data.count('District of Columbia') +
                          original_data.count('D.C.') +
                          original_data.count('"district_of_columbia"') -
                          normalized_json.count('"dc"'))

            # Write normalized data back
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(normalized_data, f, indent=2, ensure_ascii=False)

            return (file_path, True, f"Normalized {changes_count} state references", changes_count)
        else:
            return (file_path, True, "No changes needed", 0)

    except json.JSONDecodeError as e:
        return (file_path, False, f"JSON decode error: {str(e)}", 0)
    except Exception as e:
        return (file_path, False, f"Error: {str(e)}", 0)


def process_files_parallel(file_paths: List[Path], max_workers: int = None) -> Dict[str, Any]:
    """
    Process JSON files in parallel using ProcessPoolExecutor.

    Args:
        file_paths: List of JSON file paths to process
        max_workers: Maximum number of worker processes (None = auto-detect)

    Returns:
        Dictionary with processing results
    """
    if max_workers is None:
        max_workers = get_optimal_worker_count()

    results = {
        "total_files": len(file_paths),
        "processed": 0,
        "succeeded": 0,
        "failed": 0,
        "total_changes": 0,
        "files_changed": 0,
        "errors": [],
        "start_time": datetime.now().isoformat(),
    }

    print(f"\nProcessing {len(file_paths)} JSON files in parallel...")
    print(f"Using {max_workers} worker processes\n")

    start_time = time.time()

    # Process files in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(normalize_json_file, file_path): file_path
            for file_path in file_paths
        }

        # Process completed tasks
        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            results["processed"] += 1

            try:
                file_path_result, success, message, changes_count = future.result()

                if success:
                    results["succeeded"] += 1
                    if changes_count > 0:
                        results["files_changed"] += 1
                        results["total_changes"] += changes_count
                        print(f"✓ {file_path_result.name}: {message}")
                    else:
                        if results["processed"] % 10 == 0:
                            print(f"  Processed {results['processed']}/{results['total_files']} files...")
                else:
                    results["failed"] += 1
                    results["errors"].append({
                        "file": str(file_path_result),
                        "error": message
                    })
                    print(f"✗ {file_path_result.name}: {message}")

            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "file": str(file_path),
                    "error": str(e)
                })
                print(f"✗ {file_path.name}: Exception - {str(e)}")

    elapsed_time = time.time() - start_time
    results["end_time"] = datetime.now().isoformat()
    results["elapsed_seconds"] = elapsed_time

    return results


def normalize_code_files() -> Dict[str, Any]:
    """
    Normalize state references in Python code files.

    Returns:
        Dictionary with normalization results
    """
    results = {
        "files_processed": 0,
        "files_changed": 0,
        "replacements": 0,
        "errors": []
    }

    # Find Python files that might contain state references
    python_files = list(PROJECT_ROOT.rglob('*.py'))
    python_files = [f for f in python_files if '.git' not in str(f) and 'venv' not in str(f)]

    print(f"\nNormalizing state references in {len(python_files)} Python files...")

    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            replacements = 0

            # Replace common patterns
            for old_pattern, new_pattern in [
                ('"dc"', '"dc"'),
                ("'dc'", "'dc'"),
                ('"dc"', '"dc"'),
                ("'dc'", "'dc'"),
            ]:
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)
                    replacements += content.count(new_pattern) - original_content.count(new_pattern)

            if content != original_content:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                results["files_changed"] += 1
                results["replacements"] += replacements
                print(f"  ✓ {py_file.name}: {replacements} replacements")

            results["files_processed"] += 1

        except Exception as e:
            results["errors"].append({
                "file": str(py_file),
                "error": str(e)
            })
            print(f"  ✗ {py_file.name}: {str(e)}")

    return results


def main():
    """Main execution function."""
    print("=" * 80)
    print("Parallel Data Normalization for ARM M4 MAX")
    print("=" * 80)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Timestamp: {datetime.now().isoformat()}\n")

    # Find all JSON files
    print("Scanning for JSON files...")
    json_files = []

    # Search in key directories
    search_dirs = [
        DATA_DIR,
        RESEARCH_DIR,
        PROJECT_ROOT / "ref",
    ]

    for search_dir in search_dirs:
        if search_dir.exists():
            files = find_json_files(search_dir)
            json_files.extend(files)
            print(f"  Found {len(files)} JSON files in {search_dir.name}/")

    # Remove duplicates
    json_files = list(set(json_files))
    print(f"\nTotal unique JSON files to process: {len(json_files)}\n")

    if not json_files:
        print("No JSON files found to process.")
        return

    # Process JSON files in parallel
    json_results = process_files_parallel(json_files)

    # Normalize Python code files
    code_results = normalize_code_files()

    # Print summary
    print("\n" + "=" * 80)
    print("NORMALIZATION SUMMARY")
    print("=" * 80)
    print(f"\nJSON Files:")
    print(f"  Total processed: {json_results['processed']}")
    print(f"  Succeeded: {json_results['succeeded']}")
    print(f"  Failed: {json_results['failed']}")
    print(f"  Files changed: {json_results['files_changed']}")
    print(f"  Total changes: {json_results['total_changes']}")
    print(f"  Elapsed time: {json_results['elapsed_seconds']:.2f} seconds")

    print(f"\nPython Code Files:")
    print(f"  Files processed: {code_results['files_processed']}")
    print(f"  Files changed: {code_results['files_changed']}")
    print(f"  Replacements: {code_results['replacements']}")

    if json_results['errors'] or code_results['errors']:
        print(f"\nErrors encountered:")
        for error in json_results['errors'][:10]:  # Show first 10
            print(f"  - {error['file']}: {error['error']}")
        if len(json_results['errors']) > 10:
            print(f"  ... and {len(json_results['errors']) - 10} more errors")

    print("\n" + "=" * 80)
    print("Normalization complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
