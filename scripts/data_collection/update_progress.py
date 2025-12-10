#!/usr/bin/env python3
"""
Update Data Collection Progress

Script to automatically update progress tracking based on actual files.
"""

from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).parent.parent.parent
RESEARCH_DIR = PROJECT_ROOT / 'research'
PROGRESS_FILE = RESEARCH_DIR / 'reports/DATA_COLLECTION_PROGRESS.md'


def count_license_searches() -> dict:
    """Count completed license searches."""
    license_dir = RESEARCH_DIR / 'license_searches/data'
    
    states_complete = []
    states_partial = []
    
    # Check all state directories
    for state_dir in license_dir.iterdir():
        if state_dir.is_dir() and state_dir.name not in ['consolidated', 'bar_licenses', 'complaint_letters']:
            finding_files = list(state_dir.glob('*_finding.json'))
            # Assume 15 employees expected
            if len(finding_files) >= 15:
                states_complete.append(state_dir.name)
            elif len(finding_files) > 0:
                states_partial.append((state_dir.name, len(finding_files)))
    
    total_states = len(states_complete) + len(states_partial)
    progress_pct = round((len(states_complete) / 15) * 100) if total_states > 0 else 0
    
    return {
        'complete': len(states_complete),
        'partial': len(states_partial),
        'total': 15,
        'progress': progress_pct,
        'states_complete': states_complete,
        'states_partial': states_partial,
    }


def count_data_files(category: str) -> int:
    """Count JSON files in a category directory."""
    category_dir = RESEARCH_DIR / category
    if not category_dir.exists():
        return 0
    return len(list(category_dir.rglob('*.json')))


def update_progress_file():
    """Update the progress file with current counts."""
    if not PROGRESS_FILE.exists():
        print(f"Progress file not found: {PROGRESS_FILE}")
        return
    
    content = PROGRESS_FILE.read_text()
    
    # Update license searches
    license_stats = count_license_searches()
    content = re.sub(
        r'(\*\*Progress:\*\* )\d+% \(\d+/\d+ states complete\)',
        f'\\g<1>{license_stats["progress"]}% ({license_stats["complete"]}/{license_stats["total"]} states complete)',
        content
    )
    
    # Update progress bars
    license_bar_length = int(license_stats['progress'] / 5)
    license_bar = '█' * license_bar_length + '░' * (20 - license_bar_length)
    content = re.sub(
        r'(### 1\. Additional License Searches.*?\n```\n)[█░]+',
        f'\\g<1>{license_bar}',
        content,
        flags=re.DOTALL
    )
    
    # Update other categories
    categories = {
        'company_registrations': 2,
        'contracts': 3,
        'employees': 4,
        'complaints': 5,
        'financial': 6,
        'news': 7,
        'discrimination': 8,
        'professional': 9,
        'online': 10,
    }
    
    for category, num in categories.items():
        file_count = count_data_files(category)
        if file_count > 0:
            # Update status from "Not Started" to "Partial"
            content = re.sub(
                rf'(### {num}\. .*?\n\n\*\*Status:\*\* )❌ Not Started',
                '\\g<1>⚠️ Partial',
                content
            )
    
    PROGRESS_FILE.write_text(content)
    print("Progress file updated")


if __name__ == '__main__':
    update_progress_file()
    license_stats = count_license_searches()
    print(f"\nLicense Searches: {license_stats['complete']}/{license_stats['total']} states complete ({license_stats['progress']}%)")
