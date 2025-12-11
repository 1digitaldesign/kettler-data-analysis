# 🚀 Command Reference - Quick Access Guide

One-page reference for all progress bar and search commands.

---

## 📊 Progress Bar Commands

### Quick Checks
```bash
# Simple one-line progress
python3 scripts/data_collection/progress.py

# Status overview
python3 scripts/data_collection/status.py

# Sparkline format
python3 scripts/data_collection/progress.py sparkline

# Status badges
python3 scripts/data_collection/progress.py badges
```

### Full Dashboards
```bash
# Master dashboard
python3 scripts/data_collection/progress_master.py

# Colored display
python3 scripts/data_collection/progress_colored.py

# Live progress bar
python3 scripts/data_collection/live_progress_bar.py

# Search dashboard
python3 scripts/data_collection/search_dashboard.py
```

### Monitoring
```bash
# Auto-refresh (updates every 5s)
python3 scripts/data_collection/watch_progress.py

# Real-time monitor
python3 scripts/data_collection/progress_realtime.py
```

### Reports & Exports
```bash
# Generate HTML dashboard
python3 scripts/data_collection/generate_html_dashboard.py

# Generate markdown summary
python3 scripts/data_collection/generate_visual_summary.py

# Export JSON
python3 scripts/data_collection/progress_master.py --export json

# Export CSV
python3 scripts/data_collection/progress_master.py --export csv

# Export all formats
python3 scripts/data_collection/progress_master.py --export all
```

### Analysis
```bash
# Check notifications
python3 scripts/data_collection/progress_notifier.py

# Show history/trends
python3 scripts/data_collection/progress_with_history.py

# Completion estimate
python3 scripts/data_collection/progress_estimator.py
```

---

## 🔍 Search Commands

### Search Operations
```bash
# Search dashboard
python3 scripts/data_collection/search_dashboard.py

# Search workflow
python3 scripts/data_collection/search_workflow.py

# Search status
python3 scripts/data_collection/search_with_progress.py

# Complete license searches
python3 scripts/data_collection/complete_license_searches.py
```

### Automated Workflows
```bash
# Automated search workflow
python3 scripts/data_collection/automated_search_workflow.py

# Run all with progress
python3 scripts/data_collection/run_all_with_progress.py
```

---

## 🎨 Widget Formats

```bash
# All widget formats
python3 scripts/data_collection/progress_master.py --widget all

# Specific formats
python3 scripts/data_collection/progress_master.py --widget compact
python3 scripts/data_collection/progress_master.py --widget sparkline
python3 scripts/data_collection/progress_master.py --widget mini
python3 scripts/data_collection/progress_master.py --widget badges
python3 scripts/data_collection/progress_master.py --widget grid
```

---

## 💻 Python Integration

```python
# Import progress bar
from progress_bar_module import ProgressBar
pb = ProgressBar()
print(pb.draw_bar(pb.get_overall_progress()))

# Import widget
from progress_widget import ProgressWidget
widget = ProgressWidget()
print(widget.sparkline())

# Integration helpers
from progress_integration import print_progress, log_progress
print_progress('sparkline')
log_progress("Operation completed")
```

---

## 📈 Current Status

- **Overall:** 45.2%
- **License Searches:** 93.3%
- **Complete:** 2 categories
- **In Progress:** 5 categories
- **Not Started:** 3 categories

---

## 🎯 Most Common Commands

1. `python3 scripts/data_collection/status.py` - Quick status
2. `python3 scripts/data_collection/progress.py` - Simple progress
3. `python3 scripts/data_collection/search_dashboard.py` - Search status
4. `python3 scripts/data_collection/automated_search_workflow.py` - Full workflow

---

**Last Updated:** 2025-12-10
