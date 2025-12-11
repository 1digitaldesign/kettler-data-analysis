#!/usr/bin/env python3
"""
Check Search Completion Status

Returns 1 if search is complete, 0 if incomplete based on RESEARCH_OUTLINE.json criteria.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTLINE_FILE = PROJECT_ROOT / 'research' / 'RESEARCH_OUTLINE.json'


def load_outline() -> dict:
    """Load RESEARCH_OUTLINE.json."""
    if not OUTLINE_FILE.exists():
        raise FileNotFoundError(f"Research outline not found: {OUTLINE_FILE}")
    
    return json.loads(OUTLINE_FILE.read_text())


def check_file_pattern(pattern: str, base_path: Path) -> bool:
    """Check if file pattern matches any files."""
    if '**' in pattern:
        # Recursive glob
        parts = pattern.split('**')
        if len(parts) == 2:
            search_path = base_path / parts[0].rstrip('/')
            if search_path.exists():
                matches = list(search_path.rglob(parts[1].lstrip('/')))
                return len(matches) > 0
    elif '*' in pattern:
        # Simple glob
        file_path = base_path / pattern
        parent_dir = file_path.parent
        if parent_dir.exists():
            matches = list(parent_dir.glob(file_path.name))
            return len(matches) > 0
    else:
        # Exact file
        file_path = base_path / pattern
        return file_path.exists()
    
    return False


def check_search_completion(search_id: str) -> int:
    """
    Check if a search is complete.
    
    Returns:
        1 if complete, 0 if incomplete
    """
    outline = load_outline()
    
    if search_id not in outline['searches']:
        return 0
    
    search_def = outline['searches'][search_id]
    criteria = search_def['completion_criteria']
    data_folder = PROJECT_ROOT / search_def['data_folder']
    
    # Check required folders exist
    for folder_path in criteria.get('required_folders', []):
        folder = PROJECT_ROOT / folder_path
        if not folder.exists():
            return 0
    
    # Check required files exist
    for file_path in criteria.get('required_files', []):
        file = PROJECT_ROOT / file_path
        if not file.exists():
            return 0
    
    # Check file patterns
    file_patterns_ok = True
    for pattern in criteria.get('file_pattern_checks', []):
        if not check_file_pattern(pattern, data_folder):
            file_patterns_ok = False
            break
    
    if not file_patterns_ok:
        return 0
    
    # Check minimum file count
    if 'minimum_files' in criteria:
        min_files = criteria['minimum_files']
        if data_folder.exists():
            json_files = list(data_folder.rglob('*.json'))
            if len(json_files) < min_files:
                return 0
    
    # Check required states (if applicable)
    if 'required_states' in criteria and search_def.get('subdirectories', {}).get('by_state', False):
        required_states = criteria['required_states']
        for state in required_states:
            state_dir = data_folder / state
            if not state_dir.exists():
                return 0
    
    return 1


def get_all_completion_status() -> dict:
    """
    Get completion status for all searches.
    
    Returns:
        Dictionary mapping search_id to completion status (1 or 0)
    """
    outline = load_outline()
    status = {}
    
    for search_id in outline['searches']:
        status[search_id] = check_search_completion(search_id)
    
    return status


def validate_data_folders() -> dict:
    """
    Validate that all required data folders exist and are structured correctly.
    
    Returns:
        Dictionary with validation results
    """
    outline = load_outline()
    validation = {
        'valid': True,
        'folders': {},
        'errors': []
    }
    
    for search_id, search_def in outline['searches'].items():
        data_folder = PROJECT_ROOT / search_def['data_folder']
        folder_status = {
            'exists': data_folder.exists(),
            'path': str(data_folder.relative_to(PROJECT_ROOT)),
            'valid': True
        }
        
        if not data_folder.exists():
            folder_status['valid'] = False
            validation['valid'] = False
            validation['errors'].append(f"Data folder missing: {search_def['data_folder']}")
        
        validation['folders'][search_id] = folder_status
    
    return validation


def main():
    """Main function."""
    import sys
    
    if len(sys.argv) > 1:
        search_id = sys.argv[1]
        status = check_search_completion(search_id)
        print(status)
        sys.exit(0 if status == 1 else 1)
    else:
        # Print all statuses
        statuses = get_all_completion_status()
        validation = validate_data_folders()
        
        print("Search Completion Status:")
        print("=" * 60)
        
        for search_id, status in statuses.items():
            outline = load_outline()
            search_name = outline['searches'][search_id]['name']
            status_icon = "✅" if status == 1 else "❌"
            print(f"{status_icon} {search_id:30} {search_name:35} {status}")
        
        print("\n" + "=" * 60)
        total = len(statuses)
        completed = sum(statuses.values())
        print(f"Overall: {completed}/{total} searches complete ({completed/total*100:.1f}%)")
        
        if not validation['valid']:
            print("\nValidation Errors:")
            for error in validation['errors']:
                print(f"  ❌ {error}")
        
        return 0 if completed == total else 1


if __name__ == '__main__':
    exit(main())
