# 📊 Progress Bar Guide

Complete guide to all progress tracking tools available for data collection monitoring.

---

## 🚀 Quick Start

### View Progress Instantly
```bash
# Enhanced visual progress bar
python3 scripts/data_collection/live_progress_bar.py

# Simple terminal progress
python3 scripts/data_collection/show_progress.py

# Auto-refreshing watch mode (updates every 5 seconds)
python3 scripts/data_collection/watch_progress.py
```

### Generate Reports
```bash
# Generate HTML dashboard
python3 scripts/data_collection/generate_html_dashboard.py

# Generate markdown summary
python3 scripts/data_collection/generate_visual_summary.py

# Generate both reports
python3 scripts/data_collection/generate_html_dashboard.py && \
python3 scripts/data_collection/generate_visual_summary.py
```

---

## 📋 Available Tools

### 1. **Live Progress Bar** (`live_progress_bar.py`)
**Best for:** Detailed visual progress with enhanced formatting

**Features:**
- Box-drawing characters for clean borders
- Gradient-style progress bars (█▉▊▋░)
- Time estimates based on progress
- Detailed category breakdown
- Real-time statistics

**Usage:**
```bash
python3 scripts/data_collection/live_progress_bar.py
```

**Output:** Terminal display with:
- Overall progress bar (60 characters wide)
- Status breakdown (Complete/In Progress/Not Started)
- Category details with file counts
- Time estimates

---

### 2. **Watch Mode** (`watch_progress.py`)
**Best for:** Continuous monitoring with auto-refresh

**Features:**
- Auto-refreshes every 5 seconds
- Shows top 5 categories by progress
- Graceful exit with Ctrl+C
- Real-time updates

**Usage:**
```bash
python3 scripts/data_collection/watch_progress.py
```

**Output:** Continuously updating terminal display

**Stop:** Press `Ctrl+C`

---

### 3. **Simple Progress** (`show_progress.py`)
**Best for:** Quick overview without extra formatting

**Features:**
- Simple ASCII progress bars
- Task breakdown statistics
- Quick category overview

**Usage:**
```bash
python3 scripts/data_collection/show_progress.py
```

---

### 4. **HTML Dashboard** (`generate_html_dashboard.py`)
**Best for:** Visual browser-based dashboard

**Features:**
- Beautiful gradient design
- Interactive progress bars
- Color-coded status indicators
- Responsive layout
- Opens in browser automatically

**Usage:**
```bash
python3 scripts/data_collection/generate_html_dashboard.py
open outputs/reports/progress_dashboard.html
```

**Output:** `outputs/reports/progress_dashboard.html`

---

### 5. **Markdown Summary** (`generate_visual_summary.py`)
**Best for:** Documentation and version control

**Features:**
- Concise markdown format
- Progress bars for each category
- Quick stats overview
- Links to related reports
- Git-friendly format

**Usage:**
```bash
python3 scripts/data_collection/generate_visual_summary.py
```

**Output:** `research/reports/VISUAL_PROGRESS_SUMMARY.md`

---

## 📈 Current Progress Categories

1. **License Searches** - State-by-state license verification
2. **Company Registrations** - Business entity searches
3. **Employee Roles** - Organizational documentation
4. **Property Contracts** - Management agreements
5. **Regulatory Complaints** - State complaint databases
6. **Financial Records** - Public financial filings
7. **News Coverage** - Media and press coverage
8. **Fair Housing** - Discrimination records
9. **Professional Memberships** - Association memberships
10. **Social Media** - Online presence documentation

---

## 🎯 Progress Status Meanings

- **✅ Complete** - All tasks finished for this category
- **⚠️ In Progress** - Active work ongoing
- **📝 Templates Ready** - Templates created, data collection ready
- **❌ Not Started** - No work begun yet

---

## 💡 Tips

1. **For Quick Checks:** Use `live_progress_bar.py`
2. **For Continuous Monitoring:** Use `watch_progress.py`
3. **For Presentations:** Use the HTML dashboard
4. **For Documentation:** Use the markdown summary
5. **For Automation:** Run report generators in your workflow

---

## 🔄 Integration

### Add to Your Workflow
```bash
# After completing data collection tasks
python3 scripts/data_collection/generate_html_dashboard.py
python3 scripts/data_collection/generate_visual_summary.py

# View progress
python3 scripts/data_collection/live_progress_bar.py
```

### Auto-Update on File Changes
The progress bars automatically detect file changes in the `research/` directory structure. No manual updates needed!

---

## 📊 Progress Calculation

Progress is calculated based on:
- **License Searches:** States completed (15 total)
- **Company Registrations:** Files completed (12 total)
- **Employee Roles:** Files completed (2 total)
- **Other Categories:** Templates created vs. expected templates

Overall progress is the average of all category progress percentages.

---

## 🛠️ Troubleshooting

**Progress not updating?**
- Check that files are in the correct directories
- Verify file sizes (templates are < 500 bytes)
- Run `generate_visual_summary.py` to refresh stats

**HTML dashboard not opening?**
- Check file exists: `outputs/reports/progress_dashboard.html`
- Manually open: `open outputs/reports/progress_dashboard.html`

**Watch mode not working?**
- Ensure terminal supports ANSI escape codes
- Try `live_progress_bar.py` instead for one-time display

---

## 📝 Files Generated

- `outputs/reports/progress_dashboard.html` - HTML dashboard
- `research/reports/VISUAL_PROGRESS_SUMMARY.md` - Markdown summary
- `research/reports/DATA_COLLECTION_PROGRESS.md` - Detailed progress report

---

**Last Updated:** 2025-12-10
**Status:** All progress tracking tools active and operational
