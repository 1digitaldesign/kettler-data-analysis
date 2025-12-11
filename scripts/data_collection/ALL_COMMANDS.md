# 🚀 All Commands - Complete Reference

Complete command reference for the progress bar and search system.

---

## 📊 Progress Bar Commands

### Quick Access
```bash
# Simple progress (default)
python3 scripts/data_collection/progress.py

# Status overview
python3 scripts/data_collection/status.py

# Show all information
python3 scripts/data_collection/show_all.py
```

### Widget Formats
```bash
# Sparkline
python3 scripts/data_collection/progress.py sparkline

# Badges
python3 scripts/data_collection/progress.py badges

# Compact
python3 scripts/data_collection/progress.py compact

# All formats
python3 scripts/data_collection/progress_master.py --widget all
```

### Dashboards
```bash
# Master dashboard
python3 scripts/data_collection/progress_master.py

# Colored dashboard
python3 scripts/data_collection/progress_colored.py

# Live progress bar
python3 scripts/data_collection/live_progress_bar.py

# Search dashboard
python3 scripts/data_collection/search_dashboard.py
```

### Monitoring
```bash
# Auto-refresh (5s intervals)
python3 scripts/data_collection/watch_progress.py

# Real-time monitor
python3 scripts/data_collection/progress_realtime.py
```

### Reports & Exports
```bash
# HTML dashboard
python3 scripts/data_collection/generate_html_dashboard.py

# Markdown summary
python3 scripts/data_collection/generate_visual_summary.py

# Export JSON
python3 scripts/data_collection/progress_master.py --export json

# Export CSV
python3 scripts/data_collection/progress_master.py --export csv

# Export all
python3 scripts/data_collection/progress_master.py --export all
```

### Analysis
```bash
# Check notifications
python3 scripts/data_collection/progress_notifier.py

# Show history
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
# Automated workflow
python3 scripts/data_collection/automated_search_workflow.py

# Run all with progress
python3 scripts/data_collection/run_all_with_progress.py
```

---

## 🧪 Testing

```bash
# Test system
python3 scripts/data_collection/test_system.py
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

---

## 🎯 Most Common Commands

1. `python3 scripts/data_collection/show_all.py` - Complete overview
2. `python3 scripts/data_collection/status.py` - Quick status
3. `python3 scripts/data_collection/progress.py` - Simple progress
4. `python3 scripts/data_collection/search_dashboard.py` - Search status

---

**Last Updated:** 2025-12-10
