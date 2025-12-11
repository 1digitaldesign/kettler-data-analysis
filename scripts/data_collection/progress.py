#!/usr/bin/env python3
"""
Unified Progress Bar Entry Point
Single command for all progress bar needs.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        # Default: show simple progress
        from progress_simple import show_simple
        show_simple()
        return

    command = sys.argv[1].lower()

    if command in ['help', '-h', '--help']:
        show_help()
    elif command == 'simple' or command == 'bar':
        from progress_simple import show_simple
        show_simple()
    elif command == 'sparkline':
        from progress_simple import show_sparkline
        show_sparkline()
    elif command == 'badges':
        from progress_simple import show_badges
        show_badges()
    elif command == 'compact':
        from progress_simple import show_compact
        show_compact()
    elif command == 'master' or command == 'dashboard':
        from progress_master import main as master_main
        master_main()
    elif command == 'colored':
        from progress_colored import ColoredProgressBar
        cpb = ColoredProgressBar()
        cpb.display_colored_dashboard()
    elif command == 'watch':
        from watch_progress import main as watch_main
        watch_main()
    elif command == 'notify':
        from progress_notifier import ProgressNotifier
        notifier = ProgressNotifier()
        notifier.display_notifications()
    elif command == 'history':
        from progress_with_history import ProgressHistory
        ph = ProgressHistory()
        ph.display_trend()
    elif command == 'estimate':
        from progress_estimator import ProgressEstimator
        estimator = ProgressEstimator()
        estimator.display_estimate()
    elif command == 'export':
        from progress_bar_module import ProgressBar
        pb = ProgressBar()
        if len(sys.argv) > 2 and sys.argv[2] == 'csv':
            path = pb.export_csv()
            print(f"✅ Exported to: {path}")
        else:
            path = pb.export_json()
            print(f"✅ Exported to: {path}")
    elif command == 'realtime':
        from progress_realtime import RealTimeProgress
        rt = RealTimeProgress()
        rt.monitor(interval=2)
    else:
        print(f"Unknown command: {command}")
        print("Use 'progress help' for usage information")

def show_help():
    """Show help information."""
    print("""
Progress Bar System - Unified Entry Point
==========================================

Usage: progress [command] [options]

Commands:
  (no args)     Show simple progress bar (default)
  simple        Show simple progress bar
  sparkline     Show sparkline format
  badges        Show status badges
  compact       Show compact format
  master        Show master dashboard (with options)
  dashboard     Alias for master
  colored       Show colored progress dashboard
  watch         Auto-refresh mode (updates every 5s)
  notify        Check milestone notifications
  history       Show progress history and trends
  estimate      Show completion time estimate
  export        Export progress data (json/csv)
  realtime      Real-time progress monitor
  help          Show this help message

Examples:
  progress                    # Simple progress bar
  progress sparkline          # Sparkline format
  progress master --all       # Show all features
  progress watch              # Auto-refresh mode
  progress export csv         # Export to CSV
  progress notify             # Check notifications

For more options with master command:
  progress master --help
""")

if __name__ == "__main__":
    main()
