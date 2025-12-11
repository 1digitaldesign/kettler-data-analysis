#!/usr/bin/env python3
"""
Generate Consolidation View

Scans all search data folders and creates a consolidated view with statistics,
completion status, and cross-references.
"""

import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTLINE_FILE = PROJECT_ROOT / 'RESEARCH_OUTLINE.json'
CONSOLIDATION_FILE = PROJECT_ROOT / 'research' / 'CONSOLIDATION_VIEW.json'


def load_outline() -> dict:
    """Load RESEARCH_OUTLINE.json."""
    outline_path = PROJECT_ROOT / 'research' / 'RESEARCH_OUTLINE.json'
    if not outline_path.exists():
        raise FileNotFoundError(f"Research outline not found: {outline_path}")

    return json.loads(outline_path.read_text())


def count_files(directory: Path, pattern: str = "*.json") -> int:
    """Count files matching pattern in directory."""
    if not directory.exists():
        return 0

    if '**' in pattern:
        return len(list(directory.rglob(pattern.replace('**/', ''))))
    elif '*' in pattern:
        return len(list(directory.glob(pattern)))
    else:
        return 1 if (directory / pattern).exists() else 0


def get_file_list(directory: Path, pattern: str = "*.json") -> list:
    """Get list of files matching pattern."""
    if not directory.exists():
        return []

    if '**' in pattern:
        files = list(directory.rglob(pattern.replace('**/', '')))
    elif '*' in pattern:
        files = list(directory.glob(pattern))
    else:
        file_path = directory / pattern
        files = [file_path] if file_path.exists() else []

    return [str(f.relative_to(PROJECT_ROOT)) for f in files]


def check_completion_status(search_id: str, outline: dict) -> int:
    """Check completion status (1=complete, 0=incomplete)."""
    # Import the completion checker
    import sys
    sys.path.insert(0, str(PROJECT_ROOT / 'scripts' / 'research'))
    from check_search_completion import check_search_completion

    return check_search_completion(search_id)


def generate_consolidation_view() -> dict:
    """Generate consolidated view of all searches."""
    outline = load_outline()

    consolidation = {
        "_metadata": {
            "generated": datetime.now().isoformat(),
            "version": "1.0.0",
            "description": "Consolidated view of all research searches with statistics and completion status"
        },
        "overall_summary": {
            "total_searches": len(outline['searches']),
            "completed_searches": 0,
            "incomplete_searches": 0,
            "completion_percentage": 0.0,
            "total_files": 0,
            "total_data_size_mb": 0.0
        },
        "searches": {},
        "cross_references": {
            "by_priority": {},
            "by_completion": {},
            "by_data_folder": {}
        }
    }

    total_files = 0
    completed_count = 0

    for search_id, search_def in outline['searches'].items():
        data_folder = PROJECT_ROOT / search_def['data_folder']

        # Count files
        file_count = count_files(data_folder, "*.json")
        total_files += file_count

        # Get file list
        file_list = get_file_list(data_folder, "*.json")

        # Check completion status
        completion_status = check_completion_status(search_id, outline)
        if completion_status == 1:
            completed_count += 1

        # Calculate data size
        data_size = 0
        if data_folder.exists():
            for file_path in data_folder.rglob('*.json'):
                if file_path.is_file():
                    data_size += file_path.stat().st_size

        search_summary = {
            "id": search_id,
            "name": search_def['name'],
            "description": search_def['description'],
            "priority": search_def['priority'],
            "data_folder": search_def['data_folder'],
            "completion_status": completion_status,
            "file_count": file_count,
            "data_size_bytes": data_size,
            "data_size_mb": round(data_size / (1024 * 1024), 2),
            "files": file_list[:10],  # First 10 files as sample
            "total_files": len(file_list),
            "completion_criteria": search_def['completion_criteria']
        }

        consolidation['searches'][search_id] = search_summary

        # Build cross-references
        priority = search_def['priority']
        if priority not in consolidation['cross_references']['by_priority']:
            consolidation['cross_references']['by_priority'][priority] = []
        consolidation['cross_references']['by_priority'][priority].append(search_id)

        completion_key = "complete" if completion_status == 1 else "incomplete"
        if completion_key not in consolidation['cross_references']['by_completion']:
            consolidation['cross_references']['by_completion'][completion_key] = []
        consolidation['cross_references']['by_completion'][completion_key].append(search_id)

        data_folder_str = search_def['data_folder']
        if data_folder_str not in consolidation['cross_references']['by_data_folder']:
            consolidation['cross_references']['by_data_folder'][data_folder_str] = []
        consolidation['cross_references']['by_data_folder'][data_folder_str].append(search_id)

    # Update overall summary
    consolidation['overall_summary']['completed_searches'] = completed_count
    consolidation['overall_summary']['incomplete_searches'] = len(outline['searches']) - completed_count
    consolidation['overall_summary']['completion_percentage'] = round(
        (completed_count / len(outline['searches'])) * 100, 1
    )
    consolidation['overall_summary']['total_files'] = total_files

    # Calculate total data size
    total_data_size = sum(
        s['data_size_bytes'] for s in consolidation['searches'].values()
    )
    consolidation['overall_summary']['total_data_size_mb'] = round(
        total_data_size / (1024 * 1024), 2
    )

    return consolidation


def main():
    """Main function."""
    print("Generating consolidation view...")

    consolidation = generate_consolidation_view()

    # Write to file
    CONSOLIDATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONSOLIDATION_FILE.write_text(json.dumps(consolidation, indent=2) + '\n')

    print(f"✓ Consolidation view generated: {CONSOLIDATION_FILE}")
    print(f"\nOverall Summary:")
    print(f"  Total Searches: {consolidation['overall_summary']['total_searches']}")
    print(f"  Completed: {consolidation['overall_summary']['completed_searches']}")
    print(f"  Incomplete: {consolidation['overall_summary']['incomplete_searches']}")
    print(f"  Completion: {consolidation['overall_summary']['completion_percentage']}%")
    print(f"  Total Files: {consolidation['overall_summary']['total_files']}")
    print(f"  Total Size: {consolidation['overall_summary']['total_data_size_mb']} MB")


if __name__ == '__main__':
    main()
