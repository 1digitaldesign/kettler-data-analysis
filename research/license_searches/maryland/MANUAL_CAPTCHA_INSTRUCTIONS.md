# Maryland DLLR - Manual CAPTCHA Search Instructions

**Date:** December 7, 2025
**URL:** https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name

## Process Overview

This document outlines the process for searching Maryland licenses with manual CAPTCHA completion.

## Step-by-Step Process

### 1. Navigate to Search Page
```
URL: https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name
```

### 2. For Each Employee:

#### A. Fill Search Form
- **Last Name:** Enter employee's last name (required)
- **City Name:** Leave blank or enter city if known (optional)

#### B. Complete CAPTCHA
- Click the "I'm not a robot" checkbox
- Complete any image challenges if presented
- Wait for Search button to become enabled

#### C. Execute Search
- Click the "Search" button
- Wait for results page to load

#### D. Extract Results
- Check if employee name appears in results
- Note license number, status, expiration date if found
- Document "No results found" if employee not listed

### 3. Document Results

Update `maryland_search_framework.json` with:
- `captcha_completed`: true
- `search_executed`: true
- `results_found`: "yes" or "no"
- `license_details`: (if found)

## Priority Order

### HIGH PRIORITY (Complete First)
1. **Edward Hyland** - Known unlicensed in VA, critical for investigation
2. **Robert Kettler** - Company owner, critical for investigation
3. **Caitlin Skidmore** - Known licensed in DC, verify MD status

### MEDIUM PRIORITY
4-15. Remaining 12 employees

## Automation Script Support

The Playwright script can:
1. Navigate to the page
2. Fill in the Last Name field
3. **WAIT** for you to manually complete CAPTCHA
4. Detect when Search button becomes enabled
5. Click Search button
6. Extract results

### Example Playwright Code:
```javascript
// Navigate and fill form
await page.goto('https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name');
await page.fill('input[name="last_name"]', 'Hyland');

// Wait for manual CAPTCHA completion (button becomes enabled)
await page.waitForFunction(
  () => {
    const button = document.querySelector('button[type="submit"], input[type="submit"]');
    return button && !button.disabled;
  },
  { timeout: 300000 } // 5 minute timeout
);

// Click search
await page.click('button[type="submit"], input[type="submit"]');

// Extract results
const results = await page.evaluate(() => {
  // Extract license information from results page
});
```

## Alternative: CAPTCHA Solving Service

If manual completion is too time-consuming, consider:

1. **2Captcha** - https://2captcha.com
   - Cost: ~$2.99 per 1000 CAPTCHAs
   - API integration available
   - Success rate: ~95%

2. **Anti-Captcha** - https://anti-captcha.com
   - Cost: ~$1.00 per 1000 CAPTCHAs
   - Fast processing
   - Success rate: ~98%

3. **CapSolver** - https://capsolver.com
   - Cost: ~$1.50 per 1000 CAPTCHAs
   - Good for reCAPTCHA v2
   - Success rate: ~96%

## Contact Maryland Real Estate Commission

For bulk data requests:

**Maryland Real Estate Commission**
- **Address:** 100 S. Charles Street, Tower 1, Baltimore, MD 21201
- **Phone:** 410-230-6200
- **Email:** dlmrec-labor@maryland.gov

**Request:**
- Bulk export of all active real estate licenses
- CSV/Excel format preferred
- Include: Name, License Number, Status, Expiration Date, Address

## Estimated Time

- **Manual CAPTCHA:** ~2-3 minutes per employee = 30-45 minutes total
- **CAPTCHA Service:** ~30 seconds per employee = 7-8 minutes total
- **Commission Request:** 1-2 weeks for response

## Next Steps

1. Start with HIGH PRIORITY employees (manual CAPTCHA)
2. Evaluate if CAPTCHA service is worth the cost for remaining employees
3. Submit request to Maryland Real Estate Commission for bulk data
4. Document all findings in search framework JSON
