#!/usr/bin/env python3
"""
Update Progress from Actual Files

Reads actual search result files and updates progress tracking.
"""

import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
PROGRESS_FILE = PROJECT_ROOT / 'outputs' / 'reports' / 'progress_data.json'
PROGRESS_MD = PROJECT_ROOT / 'research' / 'reports' / 'DATA_COLLECTION_PROGRESS.md'
LICENSE_DIR = PROJECT_ROOT / 'research' / 'license_searches' / 'data'

EMPLOYEES = 15
STATES_TO_TRACK = ['maryland', 'connecticut']

def count_findings(state: str) -> int:
    """Count finding files for a state."""
    state_dir = LICENSE_DIR / state
    if not state_dir.exists():
        return 0
    return len(list(state_dir.glob('*_finding.json')))

def calculate_progress() -> dict:
    """Calculate progress from actual files."""
    progress = {
        'timestamp': datetime.now().isoformat(),
        'maryland': {
            'completed': count_findings('maryland'),
            'total': EMPLOYEES,
            'percent': round(count_findings('maryland') / EMPLOYEES * 100, 1) if EMPLOYEES > 0 else 0
        },
        'connecticut': {
            'completed': count_findings('connecticut'),
            'total': EMPLOYEES,
            'percent': round(count_findings('connecticut') / EMPLOYEES * 100, 1) if EMPLOYEES > 0 else 0
        }
    }

    total_completed = progress['maryland']['completed'] + progress['connecticut']['completed']
    total_searches = EMPLOYEES * 2
    progress['overall'] = {
        'completed': total_completed,
        'total': total_searches,
        'percent': round(total_completed / total_searches * 100, 1) if total_searches > 0 else 0
    }

    return progress

def update_progress_json():
    """Update progress JSON file."""
    progress = calculate_progress()
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2) + '\n')
    return progress

def update_progress_markdown(progress: dict):
    """Update progress in markdown file."""
    md_content = PROGRESS_MD.read_text()

    # Update Maryland progress
    md_content = md_content.replace(
        '- [ ] **Maryland searches** - 1/15 employees (7%)',
        f"- [ ] **Maryland searches** - {progress['maryland']['completed']}/15 employees ({progress['maryland']['percent']}%)"
    )

    # Update Connecticut progress
    md_content = md_content.replace(
        '- [ ] **Connecticut searches** - 0/15 employees (0%)',
        f"- [ ] **Connecticut searches** - {progress['connecticut']['completed']}/15 employees ({progress['connecticut']['percent']}%)"
    )

    # Update progress bar for Maryland
    md_bars = int(progress['maryland']['percent'] / 5)
    md_bar = '█' * md_bars + '░' * (20 - md_bars)
    md_content = md_content.replace(
        '### 1. Additional License Searches ⚠️ PARTIAL',
        f"### 1. Additional License Searches ⚠️ PARTIAL\n\n**Progress:** {progress['maryland']['completed'] + progress['connecticut']['completed']}/{progress['overall']['total']} searches ({progress['overall']['percent']}%)\n\n```\n{md_bar} {progress['overall']['percent']}%\n```"
    )

    PROGRESS_MD.write_text(md_content)

def main():
    """Main function."""
    print("Updating progress from actual files...")
    progress = update_progress_json()
    update_progress_markdown(progress)
    print(f"\nProgress updated:")
    print(f"  Maryland: {progress['maryland']['completed']}/{progress['maryland']['total']} ({progress['maryland']['percent']}%)")
    print(f"  Connecticut: {progress['connecticut']['completed']}/{progress['connecticut']['total']} ({progress['connecticut']['percent']}%)")
    print(f"  Overall: {progress['overall']['completed']}/{progress['overall']['total']} ({progress['overall']['percent']}%)")

if __name__ == '__main__':
    main()
