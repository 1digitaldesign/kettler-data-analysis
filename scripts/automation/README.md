# Browser Automation Scripts

Browser automation scripts for license searches with real-time progress monitoring.

## Scripts

### Progress Monitoring

- **`license_search_monitor.py`** - Monitors progress every 1 second, updates JSON and displays progress bars
- **`update_progress_from_files.py`** - Updates progress by reading actual search result files

### Search Automation

- **`license_search_automation.py`** - General license search automation framework
- **`browser_search_maryland.py`** - Maryland-specific license searches
- **`browser_search_connecticut.py`** - Connecticut-specific license searches
- **`run_license_searches_with_monitor.py`** - Runs searches with real-time monitoring

## Usage

### Monitor Progress

```bash
# Monitor progress every 1 second
python3.14 scripts/automation/license_search_monitor.py
```

### Update Progress from Files

```bash
# Update progress by reading actual files
python3.14 scripts/automation/update_progress_from_files.py
```

### Run Searches with Monitoring

```bash
# Run searches with real-time progress updates
python3.14 scripts/automation/run_license_searches_with_monitor.py
```

## Progress Files

- **`outputs/reports/progress_data.json`** - JSON progress data (updated every 1 second)
- **`research/reports/DATA_COLLECTION_PROGRESS.md`** - Markdown progress tracker (updated on demand)

## Browser Integration

These scripts are designed to work with browser automation tools. The actual browser automation code should be integrated using:

- Playwright
- Selenium
- Puppeteer
- Or other browser automation frameworks

## Next Steps

1. Integrate actual browser automation code
2. Handle CAPTCHA challenges (Maryland)
3. Implement retry logic for failed searches
4. Add error handling and logging
