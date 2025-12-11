#!/usr/bin/env python3
"""
Run License Searches with Real-Time Progress Monitoring

Runs license searches using browser automation while monitoring progress every 1 second.
"""

import subprocess
import threading
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
MONITOR_SCRIPT = PROJECT_ROOT / 'scripts' / 'automation' / 'license_search_monitor.py'
SEARCH_SCRIPT = PROJECT_ROOT / 'scripts' / 'automation' / 'license_search_automation.py'

def run_monitor():
    """Run progress monitor in background."""
    subprocess.run(['python3.14', str(MONITOR_SCRIPT)], check=False)

def run_searches():
    """Run license searches."""
    # Import browser automation here to avoid circular imports
    # For now, this is a placeholder
    print("License searches would run here using browser automation")
    print("See license_search_automation.py for implementation")

def main():
    """Main function."""
    print("=" * 60)
    print("License Search Automation with Real-Time Monitoring")
    print("=" * 60)
    print("\nStarting progress monitor...")
    
    # Start monitor in background thread
    monitor_thread = threading.Thread(target=run_monitor, daemon=True)
    monitor_thread.start()
    
    # Give monitor time to start
    time.sleep(2)
    
    print("\nStarting license searches...")
    print("Progress will update every 1 second\n")
    
    # Run searches (this would use browser automation)
    run_searches()
    
    print("\nSearches complete. Monitor will continue running.")
    print("Press Ctrl+C to stop monitor.")

if __name__ == '__main__':
    main()
