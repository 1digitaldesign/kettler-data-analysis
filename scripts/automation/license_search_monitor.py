#!/usr/bin/env python3
"""
License Search Progress Monitor

Monitors and updates progress of license searches in real-time.
Updates progress every 1 second.
"""

import time
import json
from pathlib import Path
from datetime import datetime
from typing import dict

PROJECT_ROOT = Path(__file__).parent.parent.parent
PROGRESS_FILE = PROJECT_ROOT / 'outputs' / 'reports' / 'progress_data.json'
LICENSE_DIR = PROJECT_ROOT / 'research' / 'license_searches' / 'data'

# Employees to search
EMPLOYEES = [
    'caitlin_skidmore', 'robert_kettler', 'cindy_fisher', 'luke_davis',
    'pat_cassada', 'sean_curtin', 'edward_hyland', 'amy_groff',
    'robert_grealy', 'todd_bowen', 'djene_moyer', 'henry_ramos',
    'kristina_thoummarath', 'christina_chang', 'liddy_bisanz'
]

# States to search
STATES = {
    'maryland': {'name': 'Maryland', 'url': 'https://www.dllr.state.md.us/license/occprof/realestate.html'},
    'connecticut': {'name': 'Connecticut', 'url': 'https://www.ct.gov/dcp/cwp/view.asp?a=1621&q=274200'},
}

def count_completed_searches(state: str) -> int:
    """Count completed searches for a state."""
    state_dir = LICENSE_DIR / state
    if not state_dir.exists():
        return 0
    
    finding_files = list(state_dir.glob('*_finding.json'))
    return len(finding_files)

def calculate_progress() -> dict:
    """Calculate current progress."""
    progress = {
        'timestamp': datetime.now().isoformat(),
        'overall': {
            'total_states': len(STATES),
            'completed_states': 0,
            'total_searches': len(STATES) * len(EMPLOYEES),
            'completed_searches': 0,
            'percent': 0.0
        },
        'states': {}
    }
    
    total_completed = 0
    completed_states = 0
    
    for state_code, state_info in STATES.items():
        completed = count_completed_searches(state_code)
        total = len(EMPLOYEES)
        percent = round(completed / total * 100, 1) if total > 0 else 0.0
        
        progress['states'][state_code] = {
            'name': state_info['name'],
            'completed': completed,
            'total': total,
            'percent': percent,
            'status': 'complete' if completed >= total else 'in_progress' if completed > 0 else 'not_started'
        }
        
        total_completed += completed
        if completed >= total:
            completed_states += 1
    
    progress['overall']['completed_searches'] = total_completed
    progress['overall']['completed_states'] = completed_states
    progress['overall']['percent'] = round(total_completed / progress['overall']['total_searches'] * 100, 1) if progress['overall']['total_searches'] > 0 else 0.0
    
    return progress

def update_progress_file(progress: dict) -> None:
    """Update progress JSON file."""
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2) + '\n')

def print_progress_bar(percent: float, width: int = 40) -> str:
    """Generate progress bar string."""
    filled = int(width * percent / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f"{bar} {percent:.1f}%"

def display_progress(progress: dict) -> None:
    """Display progress in terminal."""
    print(f"\n{'='*60}")
    print(f"License Search Progress - {progress['timestamp']}")
    print(f"{'='*60}\n")
    
    overall = progress['overall']
    print(f"Overall: {overall['completed_searches']}/{overall['total_searches']} searches")
    print(f"{print_progress_bar(overall['percent'])}\n")
    
    for state_code, state_data in progress['states'].items():
        status_icon = '✅' if state_data['status'] == 'complete' else '⚠️' if state_data['status'] == 'in_progress' else '❌'
        print(f"{status_icon} {state_data['name']}: {state_data['completed']}/{state_data['total']} employees")
        print(f"   {print_progress_bar(state_data['percent'], 30)}\n")

def monitor_loop(interval: float = 1.0) -> None:
    """Monitor progress in a loop, updating every interval seconds."""
    print("Starting license search progress monitor...")
    print(f"Monitoring every {interval} second(s)")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            progress = calculate_progress()
            update_progress_file(progress)
            display_progress(progress)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitor stopped.")

if __name__ == '__main__':
    monitor_loop(1.0)
