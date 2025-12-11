#!/usr/bin/env python3
"""
All-in-One Progress & Search Command
Master command that shows everything in one comprehensive view.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def show_complete_overview():
    """Show complete overview of progress and searches."""
    from show_all import show_all
    show_all()

def show_quick_status():
    """Show quick status."""
    from status import show_status
    show_status()

def show_search_dashboard():
    """Show search dashboard."""
    from search_dashboard import display_search_dashboard
    display_search_dashboard()

def main():
    """Main command handler."""
    if len(sys.argv) == 1:
        # Default: show complete overview
        show_complete_overview()
        return

    command = sys.argv[1].lower()

    if command in ['help', '-h', '--help']:
        print("""
All-in-One Progress & Search Command
====================================

Usage: all.py [command]

Commands:
  (no args)     Show complete overview (default)
  status        Show quick status
  search        Show search dashboard
  progress      Show simple progress bar
  test          Run system test
  help          Show this help

Examples:
  python3 scripts/data_collection/all.py
  python3 scripts/data_collection/all.py status
  python3 scripts/data_collection/all.py search
""")
    elif command == 'status':
        show_quick_status()
    elif command == 'search':
        show_search_dashboard()
    elif command == 'progress':
        from progress_simple import show_simple
        show_simple()
    elif command == 'test':
        from test_system import main as test_main
        test_main()
    else:
        print(f"Unknown command: {command}")
        print("Use 'all.py help' for usage information")

if __name__ == "__main__":
    main()
