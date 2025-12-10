# License Search Automation Scripts

This directory contains automation scripts for license searches across multiple states.

## Scripts

### Connecticut License Search

**Files:**
- `connecticut_license_search.js` - Original script
- `connecticut_license_search_improved.js` - **RECOMMENDED** - Improved blank page handling

**Purpose:** Automate license searches in Connecticut DCP eLicense portal

**Features:**
- No CAPTCHA required
- Automated form filling
- Results evaluation
- Batch processing for 13 employees
- **IMPROVED:** Better blank page handling with `waitForPageLoad()` function
- **IMPROVED:** Enhanced error diagnostics and logging

**Usage:**
```javascript
// Via Playwright MCP browser_run_code
// Copy the script content and execute searchAllEmployees()
```

**License Types:**
- `REAL ESTATE BROKER` - For executives/managers
- `REAL ESTATE SALESPERSON` - For staff/property managers

### Maryland License Search

**Files:**
- `maryland_license_search.js` - Original script
- `maryland_license_search_improved.js` - **RECOMMENDED** - Improved blank page handling

**Purpose:** Automate license searches in Maryland DLLR portal

**Features:**
- Form filling automation
- Manual CAPTCHA completion wait
- Results evaluation
- Batch processing for 14 employees
- **IMPROVED:** Better blank page handling with `waitForPageLoad()` function
- **IMPROVED:** Enhanced error diagnostics and logging

**Usage:**
```javascript
// Via Playwright MCP browser_run_code
// Copy the script content and execute searchAllEmployees()
// NOTE: Requires manual CAPTCHA completion for each search
```

**CAPTCHA Handling:**
- Script waits for manual CAPTCHA completion
- Button becomes enabled when CAPTCHA is completed
- Timeout after 5 minutes if CAPTCHA not completed

## Execution Instructions

### Using Playwright MCP

1. Navigate to the state's license search page
2. Use `browser_run_code` tool with the script content
3. Execute the main function (e.g., `searchAllEmployees()`)
4. For Maryland, manually complete CAPTCHA when prompted

### Example: Connecticut

```javascript
// Navigate first
browser_navigate("https://www.elicense.ct.gov/lookup/licenselookup.aspx")

// Then run script
browser_run_code({
  code: `
    // Paste connecticut_license_search.js content here
    // Then call:
    await searchAllEmployees();
  `
})
```

### Example: Maryland

```javascript
// Navigate first
browser_navigate("https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name")

// Then run script
browser_run_code({
  code: `
    // Paste maryland_license_search.js content here
    // Then call:
    await searchAllEmployees();
    // NOTE: Manually complete CAPTCHA when script pauses
  `
})
```

## Employee Lists

### Connecticut (13 remaining)
- Caitlin Skidmore (BROKER - HIGH priority)
- Cindy Fisher (BROKER)
- Luke Davis (BROKER)
- Pat Cassada (BROKER)
- Sean Curtin (BROKER)
- Amy Groff (SALESPERSON)
- Robert Grealy (BROKER)
- Djene Moyer (SALESPERSON)
- Henry Ramos (SALESPERSON)
- Kristina Thoummarath (SALESPERSON)
- Christina Chang (SALESPERSON)
- Todd Bowen (BROKER)
- Jeffrey Williams (SALESPERSON)

### Maryland (14 remaining)
- Robert Kettler (waiting CAPTCHA - HIGH priority)
- Caitlin Skidmore (HIGH priority)
- 12 medium priority employees

## Output Format

Both scripts return results in JSON format:

```json
{
  "employee": "Employee Name",
  "searchExecuted": true,
  "results": {
    "hasTable": true,
    "exactMatch": false,
    "noResults": true,
    "licenseInfo": null,
    "pageText": "..."
  },
  "timestamp": "2025-12-07T..."
}
```

## Blank Page Troubleshooting

**Issue:** Browser automation shows blank pages

**Solution:** Use the improved scripts (`*_improved.js`) which include:
- `waitForPageLoad()` function that properly waits for page content
- Better error handling with diagnostic information
- Element visibility checks before interaction
- Increased timeout values
- Detailed logging

See `BROWSER_AUTOMATION_TROUBLESHOOTING.md` for detailed troubleshooting guide.

## Notes

- Connecticut: Fully automated, no CAPTCHA
- Maryland: Requires manual CAPTCHA completion
- Both scripts include error handling
- Results are evaluated for exact name matches
- Scripts wait between searches to avoid rate limiting
- **IMPROVED SCRIPTS:** Use `*_improved.js` versions to handle blank page issues

## DevTools Enhanced Scraping

**NEW:** DevTools-powered scraping scripts with advanced data extraction capabilities.

### Features
- Network monitoring and request tracking
- DOM inspection and structured data extraction
- Pattern matching for license information
- Performance metrics and debugging
- Comprehensive error handling

### Files
- `scrape_with_devtools.js` - Core DevTools scraping functions
- `connecticut_license_search_devtools.js` - DevTools-enhanced Connecticut script
- `devtools_scraping_guide.md` - Complete usage guide
- `README_DEVTOOLS.md` - DevTools documentation

### Usage
```javascript
const { scrapeConnecticut, extractLicenseInfo } = require('./scrape_with_devtools.js');

const result = await scrapeConnecticut(page, employee);
const licenseInfo = extractLicenseInfo(result);
```

See `README_DEVTOOLS.md` for complete documentation.

## Universal DevTools Scraper

**NEW:** Comprehensive universal scraper for all employees and all states.

### Features
- ✅ **All 6 states** supported (CT, MD, NJ, NY, DC, VA)
- ✅ **All 17 employees** included
- ✅ **Any use case** - extensible framework
- ✅ Universal functions for any scenario
- ✅ Batch processing support
- ✅ Progress tracking
- ✅ Custom extractors

### Files
- `universal_devtools_scraper.js` - Complete universal framework (32KB)
- `UNIVERSAL_SCRAPER_GUIDE.md` - Complete usage guide

### Quick Start
```javascript
const { searchAllEmployeesAllStates } = require('./universal_devtools_scraper.js');

// Search all employees in all states
const results = await searchAllEmployeesAllStates(page);
```

See `UNIVERSAL_SCRAPER_GUIDE.md` for complete documentation.

## Integration with CAPTCHA Services

For automated CAPTCHA solving in Maryland, integrate with:
- 2Captcha API
- Anti-Captcha API
- CapSolver API

See `research/license_searches/maryland/CAPTCHA_SERVICE_SETUP.md` for details.
