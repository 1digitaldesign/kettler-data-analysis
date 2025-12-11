# 🔍 Search Operations with Progress Bar Integration

Guide for integrating progress bars into search operations.

---

## ✅ Integrated Scripts

### **complete_license_searches.py**
- ✅ Progress bar integration
- ✅ Shows initial and final progress
- ✅ Updates during template creation
- ✅ Logs progress changes

### **search_with_progress.py**
- ✅ Real-time progress updates
- ✅ Search status tracking
- ✅ Progress change detection

---

## 🚀 Usage

### Run License Search Completion
```bash
python3 scripts/data_collection/complete_license_searches.py
```

This will:
1. Show current progress
2. List missing searches
3. Create templates with progress updates
4. Show final progress

### Run Search with Progress
```bash
python3 scripts/data_collection/search_with_progress.py
```

Shows:
- Current search status
- License search completion
- Missing searches breakdown

---

## 💻 Integration in Your Scripts

### Basic Integration
```python
from progress_integration import log_progress, print_progress

# Show progress before search
print_progress('sparkline')

# Perform search operations
# ... your search code ...

# Log progress after search
log_progress("Search completed")
```

### Real-time Updates
```python
from progress_realtime import RealTimeProgress

rt = RealTimeProgress()

# Show progress during search
for item in items_to_search:
    # Perform search
    perform_search(item)

    # Update progress
    rt.show_update(f"Searched {item}")
```

### Full Integration Example
```python
from search_with_progress import SearchWithProgress

swp = SearchWithProgress()

# Simulate search with progress
items = ['item1', 'item2', 'item3']
swp.simulate_search("License Search", items)
```

---

## 📊 Progress Updates

Progress bars automatically update when:
- Files are created in `research/license_searches/data/`
- Templates are created
- Search results are saved
- Data collection files are updated

---

## 🔄 Workflow

1. **Start Search**
   ```bash
   python3 scripts/data_collection/complete_license_searches.py
   ```

2. **Check Progress**
   ```bash
   python3 scripts/data_collection/progress.py
   ```

3. **Monitor Progress**
   ```bash
   python3 scripts/data_collection/watch_progress.py
   ```

4. **After Search**
   ```bash
   python3 scripts/data_collection/progress.py master --summary
   ```

---

## 📈 Current Search Status

- **License Searches:** 93.3% (14/15 states complete)
- **Missing:** Maryland (partial), Connecticut (not started)
- **Templates:** Ready for data collection

---

## 💡 Tips

1. **Before searching:** Check progress with `progress.py`
2. **During search:** Use `watch_progress.py` for monitoring
3. **After search:** Verify progress updated correctly
4. **Integration:** Use `log_progress()` in your search scripts

---

**Last Updated:** 2025-12-10
**Status:** Search scripts integrated with progress bars
