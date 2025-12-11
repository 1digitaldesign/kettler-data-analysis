#!/bin/bash
# Progress Bar Aliases
# Source this file or add to your .bashrc/.zshrc for easy access

# Navigate to project directory
cd "$(dirname "$0")/../.." || exit

# Progress bar aliases
alias progress='python3 scripts/data_collection/progress_master.py'
alias progress-bar='python3 scripts/data_collection/progress_simple.py'
alias progress-sparkline='python3 scripts/data_collection/progress_simple.py sparkline'
alias progress-badges='python3 scripts/data_collection/progress_simple.py badges'
alias progress-compact='python3 scripts/data_collection/progress_simple.py compact'
alias progress-colored='python3 scripts/data_collection/progress_colored.py'
alias progress-watch='python3 scripts/data_collection/watch_progress.py'
alias progress-notify='python3 scripts/data_collection/progress_notifier.py'
alias progress-history='python3 scripts/data_collection/progress_with_history.py'
alias progress-estimate='python3 scripts/data_collection/progress_estimator.py'
alias progress-export='python3 scripts/data_collection/progress_master.py --export all'
alias progress-all='python3 scripts/data_collection/progress_master.py --all'

# Widget formats
alias progress-widget-compact='python3 scripts/data_collection/progress_master.py --widget compact'
alias progress-widget-sparkline='python3 scripts/data_collection/progress_master.py --widget sparkline'
alias progress-widget-mini='python3 scripts/data_collection/progress_master.py --widget mini'

echo "✅ Progress bar aliases loaded!"
echo ""
echo "Available commands:"
echo "  progress              - Default dashboard"
echo "  progress-bar          - Simple progress bar"
echo "  progress-sparkline    - Sparkline format"
echo "  progress-colored      - Colorized display"
echo "  progress-watch        - Auto-refresh mode"
echo "  progress-notify       - Check notifications"
echo "  progress-history      - Show history"
echo "  progress-estimate     - Completion estimate"
echo "  progress-export       - Export all formats"
echo "  progress-all          - Show all features"
