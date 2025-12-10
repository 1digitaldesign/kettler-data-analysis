# Chrome DevTools Scraping Guide

**Purpose:** Use Chrome DevTools capabilities to enhance web scraping and data extraction

---

## DevTools Features Used

### 1. Network Monitoring
- Monitor all network requests
- Track API calls
- Identify data sources
- Debug failed requests

### 2. DOM Inspection
- Extract structured data from tables
- Parse forms and inputs
- Identify element selectors
- Analyze page structure

### 3. Console Logging
- Capture console errors
- Debug JavaScript issues
- Monitor page events
- Track performance

### 4. Performance Metrics
- Page load times
- DOM content loaded time
- Network request timing
- Resource loading analysis

---

## Usage

### Basic Scraping with DevTools

```javascript
const { scrapeWithDevTools, extractLicenseInfo } = require('./scrape_with_devtools.js');

// Scrape a page
const scrapedData = await scrapeWithDevTools(page, employee, 'Connecticut');

// Extract license information
const licenseInfo = extractLicenseInfo(scrapedData);

console.log('License found:', licenseInfo.found);
console.log('Licenses:', licenseInfo.licenses);
```

### Connecticut License Search

```javascript
const { scrapeConnecticut } = require('./scrape_with_devtools.js');

const employee = {
  name: "Caitlin Skidmore",
  lastName: "Skidmore",
  firstName: "Caitlin",
  licenseType: "REAL ESTATE BROKER"
};

const result = await scrapeConnecticut(page, employee);
const licenseInfo = extractLicenseInfo(result);
```

### Maryland License Search

```javascript
const { scrapeMaryland } = require('./scrape_with_devtools.js');

const employee = {
  name: "Caitlin Skidmore",
  lastName: "Skidmore",
  firstName: "Caitlin"
};

const result = await scrapeMaryland(page, employee);
const licenseInfo = extractLicenseInfo(result);
```

---

## Data Extraction Features

### 1. Table Extraction
- Automatically identifies all tables
- Extracts headers and data rows
- Structures data into JSON format
- Handles merged cells

### 2. License Pattern Matching
- Extracts license numbers using regex patterns
- Identifies license types
- Captures status information
- Extracts expiration dates

### 3. Results Detection
- Detects "no results" messages
- Counts matching records
- Identifies employee name matches
- Validates search success

### 4. Structured Data Output
- JSON format for easy processing
- Performance metrics included
- Network request logs
- DOM statistics

---

## Advanced Features

### Network Request Monitoring

```javascript
// Monitor all network requests
page.on('request', request => {
  console.log('Request:', request.url());
  console.log('Method:', request.method());
  console.log('Type:', request.resourceType());
});
```

### Console Error Capture

```javascript
// Capture console errors
page.on('console', msg => {
  if (msg.type() === 'error') {
    console.error('Console Error:', msg.text());
  }
});
```

### Performance Metrics

```javascript
// Get performance timing
const timing = await page.evaluate(() => {
  return window.performance.timing;
});

console.log('Load time:', timing.loadEventEnd - timing.navigationStart);
```

---

## Output Format

### Scraped Data Structure

```json
{
  "employee": "Caitlin Skidmore",
  "state": "Connecticut",
  "searchExecuted": true,
  "pageData": {
    "performance": {
      "loadTime": 1234,
      "domContentLoaded": 567,
      "pageLoad": 1234
    },
    "tables": [
      {
        "index": 0,
        "id": "results-table",
        "rowCount": 5,
        "rows": [...],
        "fullText": "..."
      }
    ],
    "licenseData": {
      "employeeName": "Caitlin Skidmore",
      "hasResults": false,
      "noResultsMessage": "No results found",
      "licenseNumbers": [],
      "licenseTypes": [],
      "statuses": []
    },
    "structuredData": [
      {
        "headers": ["Name", "License Number", "Status"],
        "dataRows": [...]
      }
    ]
  },
  "networkRequests": [...],
  "timestamp": "2025-12-08T..."
}
```

### Extracted License Info

```json
{
  "found": false,
  "noResults": true,
  "noResultsMessage": "No results found",
  "licenses": [],
  "licenseNumbers": [],
  "licenseTypes": [],
  "statuses": [],
  "expirationDates": [],
  "resultsCount": 0,
  "pageUrl": "https://...",
  "pageTitle": "..."
}
```

---

## Benefits

### 1. Better Data Extraction
- Structured table parsing
- Pattern-based license extraction
- Comprehensive data capture

### 2. Improved Reliability
- Network monitoring for debugging
- Console error capture
- Performance metrics for optimization

### 3. Enhanced Debugging
- Detailed logging
- Request/response tracking
- Performance analysis

### 4. Structured Output
- JSON format for easy processing
- Consistent data structure
- Easy integration with analysis tools

---

## Integration with Existing Scripts

The DevTools scraping functions can be integrated with existing automation scripts:

```javascript
// In connecticut_license_search_improved.js
const { scrapeWithDevTools, extractLicenseInfo } = require('./scrape_with_devtools.js');

async function searchEmployee(page, employee) {
  // ... existing code ...

  // Use DevTools scraping for better extraction
  const scrapedData = await scrapeWithDevTools(page, employee, 'Connecticut');
  const licenseInfo = extractLicenseInfo(scrapedData);

  return {
    employee: employee.name,
    licenseType: employee.licenseType,
    searchExecuted: true,
    licenseInfo: licenseInfo,
    scrapedData: scrapedData,
    timestamp: new Date().toISOString()
  };
}
```

---

## Troubleshooting

### Blank Pages
- Check network requests for failed resources
- Monitor console for JavaScript errors
- Verify page load completion

### Missing Data
- Inspect table structure
- Check for dynamic content loading
- Verify selector accuracy

### Performance Issues
- Monitor load times
- Check network request count
- Optimize wait conditions

---

**Last Updated:** December 8, 2025
**Status:** DevTools scraping functions implemented
