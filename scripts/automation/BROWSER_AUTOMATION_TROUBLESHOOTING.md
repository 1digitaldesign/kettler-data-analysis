# Browser Automation Troubleshooting Guide

**Issue:** Browser automation shows blank pages

---

## Common Causes of Blank Pages

### 1. Page Not Fully Loaded
- **Symptom:** Page appears blank immediately after navigation
- **Cause:** JavaScript hasn't finished rendering
- **Solution:** Use `waitForPageLoad()` function with proper wait conditions

### 2. Network Issues
- **Symptom:** Page stays blank, no content loads
- **Cause:** Network timeout or connection issues
- **Solution:** Increase timeout values, check network connectivity

### 3. Anti-Bot Protection
- **Symptom:** Page loads but shows blank/empty content
- **Cause:** Website detects automation and blocks content
- **Solution:** Use stealth mode, add delays, or manual intervention

### 4. JavaScript Rendering Required
- **Symptom:** HTML loads but content is blank
- **Cause:** Content requires JavaScript to render
- **Solution:** Wait for `networkidle` state and specific elements

---

## Solutions Implemented

### Improved Script Features

1. **`waitForPageLoad()` Function**
   - Waits for `networkidle` state
   - Waits for `domcontentloaded` state
   - Checks if page has content
   - Provides diagnostics on failure

2. **Better Error Handling**
   - Captures page diagnostics on errors
   - Logs URL, title, body content
   - Provides detailed error messages

3. **Element Visibility Checks**
   - Waits for elements to be visible before interaction
   - Uses `waitFor({ state: 'visible' })` instead of just `waitFor()`
   - Increases timeout values

4. **Diagnostic Information**
   - Logs page title and URL
   - Captures body content length
   - Checks document ready state

---

## Usage Instructions

### For Connecticut Searches

```javascript
// Use the improved script
const script = require('./connecticut_license_search_improved.js');

// Run searches
await script.searchAllEmployees();
```

### For Maryland Searches

```javascript
// Use the improved script (when created)
const script = require('./maryland_license_search_improved.js');

// Run searches (requires manual CAPTCHA)
await script.searchAllEmployees();
```

---

## Manual Troubleshooting Steps

### Step 1: Check Page Load
```javascript
// Navigate and wait
await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
await page.waitForLoadState('networkidle');

// Check if page has content
const hasContent = await page.evaluate(() => {
  return document.body && document.body.innerText.trim().length > 0;
});
```

### Step 2: Get Page Diagnostics
```javascript
const diagnostics = await page.evaluate(() => {
  return {
    url: window.location.href,
    title: document.title,
    bodyText: document.body ? document.body.innerText.substring(0, 200) : 'No body',
    bodyLength: document.body ? document.body.innerText.length : 0,
    readyState: document.readyState
  };
});
console.log('Page diagnostics:', diagnostics);
```

### Step 3: Wait for Specific Elements
```javascript
// Wait for form elements
await page.waitForSelector('select[name*="LicenseType"]', {
  state: 'visible',
  timeout: 15000
});
```

### Step 4: Check for Errors
```javascript
// Listen for console errors
page.on('console', msg => console.log('Console:', msg.text()));
page.on('pageerror', error => console.error('Page error:', error));
```

---

## Alternative Approaches

### 1. Use Browser Snapshot
Instead of evaluating JavaScript, use browser snapshot tool:
```javascript
// Take snapshot to see what browser sees
const snapshot = await browser_snapshot();
```

### 2. Manual Verification
If automation fails, verify manually:
1. Open browser manually
2. Navigate to URL
3. Check if page loads correctly
4. Note any CAPTCHA or blocking

### 3. Increase Timeouts
```javascript
// Increase all timeout values
await page.goto(url, { timeout: 120000 }); // 2 minutes
await page.waitForSelector(selector, { timeout: 30000 }); // 30 seconds
```

### 4. Add Delays
```javascript
// Add delays between actions
await page.waitForTimeout(5000); // 5 second delay
```

---

## Testing the Improved Script

### Test Single Search
```javascript
// Test with one employee first
const testEmployee = employees[0];
const result = await searchEmployee(page, testEmployee);
console.log('Test result:', result);
```

### Check Diagnostics
```javascript
// If blank page, check diagnostics
if (result.error || !result.results.hasContent) {
  console.log('Diagnostics:', result.diagnostics);
}
```

---

## Known Issues

### Connecticut eLicense Portal
- **Status:** Working with improved script
- **Issue:** None known
- **Solution:** Use `connecticut_license_search_improved.js`

### Maryland DLLR Portal
- **Status:** Requires CAPTCHA
- **Issue:** CAPTCHA blocks automation
- **Solution:** Manual CAPTCHA completion or CAPTCHA service

---

## Next Steps

1. **Test Improved Script:** Run `connecticut_license_search_improved.js` to verify blank page issue is resolved
2. **Create Maryland Improved Script:** Apply same improvements to Maryland script
3. **Add Diagnostics:** Include diagnostic logging in all automation scripts
4. **Document Results:** Log all blank page occurrences with diagnostics

---

**Last Updated:** December 8, 2025
**Status:** Improved scripts created with blank page handling
