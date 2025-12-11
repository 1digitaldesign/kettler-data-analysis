# 🔍 Search Workflow with Progress Bar Integration

Complete guide for performing searches with integrated progress tracking.

---

## 🚀 Quick Start

### Run Complete Search Workflow
```bash
# Full workflow with progress tracking
python3 scripts/data_collection/search_workflow.py

# Simulate searches (for testing)
python3 scripts/data_collection/search_workflow.py --simulate

# Search specific state
python3 scripts/data_collection/search_workflow.py --state maryland
```

---

## 📋 Available Search Scripts

### 1. **search_workflow.py** ⭐ Complete Workflow
**Best for:** Full search operations with progress tracking

**Features:**
- Analyzes search status
- Performs searches with progress updates
- Shows progress summary
- State-specific searches

**Usage:**
```bash
python3 scripts/data_collection/search_workflow.py
python3 scripts/data_collection/search_workflow.py --simulate
python3 scripts/data_collection/search_workflow.py --state connecticut
```

---

### 2. **complete_license_searches.py** ⭐ License Search Completion
**Best for:** Completing license searches for Maryland and Connecticut

**Features:**
- Shows initial progress
- Lists missing searches
- Creates templates with progress
- Shows final progress

**Usage:**
```bash
python3 scripts/data_collection/complete_license_searches.py
```

---

### 3. **search_with_progress.py** ⭐ Search Status Checker
**Best for:** Checking search status and progress

**Features:**
- Current progress display
- License search status
- Missing searches breakdown

**Usage:**
```bash
python3 scripts/data_collection/search_with_progress.py
```

---

## 🔄 Workflow Steps

### Step 1: Check Current Status
```bash
python3 scripts/data_collection/search_with_progress.py
```

### Step 2: Run Search Workflow
```bash
python3 scripts/data_collection/search_workflow.py
```

### Step 3: Monitor Progress
```bash
# In another terminal
python3 scripts/data_collection/watch_progress.py
```

### Step 4: Verify Completion
```bash
python3 scripts/data_collection/progress.py master --summary
```

---

## 📊 Progress Integration

All search scripts automatically:
- ✅ Show initial progress
- ✅ Update progress during operations
- ✅ Show final progress
- ✅ Log progress changes
- ✅ Refresh progress after file changes

---

## 💻 Integration in Your Scripts

### Basic Integration
```python
from search_workflow import SearchWorkflow

workflow = SearchWorkflow()
workflow.run_workflow(simulate=False)
```

### Custom Search with Progress
```python
from search_with_progress import SearchWithProgress
from progress_realtime import RealTimeProgress

swp = SearchWithProgress()
rt = RealTimeProgress()

# Perform searches
for item in items_to_search:
    perform_search(item)
    rt.show_update(f"Searched {item}")

swp.show_search_complete("License Search", len(items_to_search))
```

---

## 📈 Current Search Status

- **License Searches:** 93.3% (14/15 states)
- **Maryland:** Complete ✅
- **Connecticut:** Complete ✅
- **Overall Progress:** 45.2%

---

## 🎯 Search Categories

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

## 💡 Tips

1. **Before searching:** Check status with `search_with_progress.py`
2. **During search:** Use `watch_progress.py` for monitoring
3. **After search:** Verify with `progress.py master --summary`
4. **Integration:** Use `log_progress()` in your search scripts

---

## 🔗 Related Documentation

- `SEARCH_INTEGRATION.md` - Integration guide
- `README_PROGRESS_BARS.md` - Progress bar system
- `USAGE_EXAMPLES.md` - Usage examples

---

**Last Updated:** 2025-12-10
**Status:** Search workflow integrated with progress bars
