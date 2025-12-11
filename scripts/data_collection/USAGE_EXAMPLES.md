# 📊 Progress Bar Usage Examples

Quick reference for common progress bar use cases.

---

## 🚀 Most Common Commands

### Quick Check (One Line)
```bash
python3 scripts/data_collection/progress_simple.py
```
Output: `█████████████░░░░░░░░░░░░░░░░░ 45.2% | ✅2 ⚠️5 ❌3`

### Sparkline Format
```bash
python3 scripts/data_collection/progress_simple.py sparkline
```
Output: `█████████░░░░░░░░░░░ 45.2%`

### Full Dashboard
```bash
python3 scripts/data_collection/progress_master.py
```

---

## 💻 In Your Python Scripts

### Simple Integration
```python
from progress_integration import print_progress

# Add to your script
print_progress('sparkline')
```

### With Logging
```python
from progress_integration import log_progress

# Log progress with timestamp
log_progress("After data collection step")
```

### Get Progress Data
```python
from progress_integration import get_progress_dict

progress = get_progress_dict()
print(f"Overall: {progress['overall']:.1f}%")
print(f"Complete: {progress['status_counts']['complete']}")
```

---

## 📊 Widget Formats

```bash
# Compact
python3 scripts/data_collection/progress_master.py --widget compact

# Sparkline
python3 scripts/data_collection/progress_master.py --widget sparkline

# Mini Dashboard
python3 scripts/data_collection/progress_master.py --widget mini

# Badges
python3 scripts/data_collection/progress_master.py --widget badges

# All formats
python3 scripts/data_collection/progress_master.py --widget all
```

---

## 🔔 Notifications & Tracking

```bash
# Check milestones
python3 scripts/data_collection/progress_notifier.py

# Show history
python3 scripts/data_collection/progress_with_history.py

# Completion estimate
python3 scripts/data_collection/progress_estimator.py
```

---

## 📤 Export Data

```bash
# Export JSON
python3 scripts/data_collection/progress_master.py --export json

# Export CSV
python3 scripts/data_collection/progress_master.py --export csv

# Export both
python3 scripts/data_collection/progress_master.py --export all
```

---

## 🎨 Colored Display

```bash
python3 scripts/data_collection/progress_colored.py
```

---

## 🔄 Auto-Refresh

```bash
# Watch mode (updates every 5 seconds)
python3 scripts/data_collection/watch_progress.py
# Press Ctrl+C to stop
```

---

## 📈 Current Status

- **Overall:** 45.2%
- **Complete:** 2 categories
- **In Progress:** 5 categories
- **Not Started:** 3 categories

---

## 💡 Tips

1. **For quick checks:** Use `progress_simple.py`
2. **For scripts:** Use `progress_integration.py` functions
3. **For monitoring:** Use `watch_progress.py`
4. **For reports:** Use `generate_html_dashboard.py`
5. **For exports:** Use `progress_master.py --export`

---

**Last Updated:** 2025-12-10
