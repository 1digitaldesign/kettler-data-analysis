# 🚀 Progress Bar Quick Reference

One-page quick reference for all progress bar commands.

---

## 📊 Master Command (Recommended)

```bash
# Default dashboard
python3 scripts/data_collection/progress_master.py

# All features
python3 scripts/data_collection/progress_master.py --all

# Widget formats
python3 scripts/data_collection/progress_master.py --widget compact
python3 scripts/data_collection/progress_master.py --widget sparkline
python3 scripts/data_collection/progress_master.py --widget mini

# Check notifications
python3 scripts/data_collection/progress_master.py --notify

# Show history
python3 scripts/data_collection/progress_master.py --history

# Export data
python3 scripts/data_collection/progress_master.py --export json
python3 scripts/data_collection/progress_master.py --export csv
```

---

## 🎨 Individual Tools

### Display Tools
```bash
# Enhanced visual display
python3 scripts/data_collection/live_progress_bar.py

# Auto-refresh (5s intervals)
python3 scripts/data_collection/watch_progress.py

# Simple display
python3 scripts/data_collection/show_progress.py
```

### Widgets
```bash
# All widget formats
python3 scripts/data_collection/progress_widget.py
```

### Tracking & Notifications
```bash
# Record history snapshot
python3 scripts/data_collection/progress_with_history.py

# Check milestones
python3 scripts/data_collection/progress_notifier.py
```

### Reports
```bash
# HTML dashboard
python3 scripts/data_collection/generate_html_dashboard.py
open outputs/reports/progress_dashboard.html

# Markdown summary
python3 scripts/data_collection/generate_visual_summary.py
```

---

## 💻 Python Integration

```python
# Import ProgressBar
from progress_bar_module import ProgressBar
pb = ProgressBar()
print(pb.draw_bar(pb.get_overall_progress()))

# Import Widget
from progress_widget import ProgressWidget
widget = ProgressWidget()
print(widget.compact_bar())

# Import Notifier
from progress_notifier import ProgressNotifier
notifier = ProgressNotifier()
notifier.display_notifications()
```

---

## 📁 Output Files

- `outputs/reports/progress_dashboard.html` - HTML dashboard
- `outputs/reports/progress_data.json` - JSON export
- `outputs/reports/progress_data.csv` - CSV export
- `outputs/reports/progress_history.json` - History data
- `outputs/reports/progress_notifications.json` - Notifications
- `research/reports/VISUAL_PROGRESS_SUMMARY.md` - Markdown summary

---

## 🎯 Widget Formats

| Format | Command |
|--------|---------|
| Compact | `--widget compact` |
| Mini Dashboard | `--widget mini` |
| Inline | `--widget inline` |
| Sparkline | `--widget sparkline` |
| Circle | `--widget circle` |
| Badges | `--widget badges` |
| Grid | `--widget grid` |
| All | `--widget all` |

---

## 📈 Current Status

- **Overall:** 45.2%
- **Complete:** 2 categories
- **In Progress:** 5 categories
- **Not Started:** 3 categories
- **Next Milestone:** 50% (4.8% away)

---

## 🔗 Documentation

- `README_PROGRESS_BARS.md` - Complete guide
- `PROGRESS_BAR_GUIDE.md` - Usage guide
- `PROGRESS_BAR_FEATURES.md` - Features documentation
- `QUICK_REFERENCE.md` - This file

---

**Last Updated:** 2025-12-10
