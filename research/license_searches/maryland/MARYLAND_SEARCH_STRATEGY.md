# Maryland License Search - Complete Strategy

**Date:** December 7, 2025
**Status:** Ready for Implementation

## Summary

Maryland DLLR requires reCAPTCHA v2 for all license searches. We have identified multiple approaches to handle this requirement.

## Recommended Approach: Hybrid Strategy

### Phase 1: Manual CAPTCHA (Immediate - High Priority)
**Target:** Edward Hyland, Robert Kettler, Caitlin Skidmore

**Process:**
1. Use Playwright to navigate and fill form
2. Manually complete CAPTCHA
3. Script waits for button enablement
4. Script continues automation
5. Extract results

**Time:** ~10 minutes for 3 employees

### Phase 2: CAPTCHA Service (Short-term - Remaining Employees)
**Target:** Remaining 12 employees

**Service:** 2Captcha or Anti-Captcha
**Cost:** ~$0.03 per search = $0.36 total
**Time:** ~10 minutes for 12 employees

**Implementation:**
- Integrate CAPTCHA solving API
- Automated search for all remaining employees
- Extract and document results

### Phase 3: Commission Request (Long-term - Backup)
**Target:** All employees (if service fails or for verification)

**Action:** Email Maryland Real Estate Commission
**Request:** Bulk license data export
**Timeline:** 1-2 weeks for response

## Technical Implementation

### Manual CAPTCHA Wait Function
```javascript
// Wait for CAPTCHA completion
await page.waitForFunction(
  () => {
    const button = document.querySelector('button[type="submit"], input[type="submit"]');
    return button && !button.disabled;
  },
  { timeout: 300000 } // 5 minutes
);
```

### CAPTCHA Service Integration
```javascript
// Using 2Captcha
const { solveRecaptcha } = require('playwright-recaptcha');
await solveRecaptcha(page, {
  apiKey: 'YOUR_API_KEY',
  provider: '2captcha'
});
```

## Contact Information

**Maryland Real Estate Commission**
- Email: dlmrec-labor@maryland.gov
- Phone: 410-230-6200
- Address: 100 S. Charles Street, Tower 1, Baltimore, MD 21201

## Files Created

1. `maryland_search_framework.json` - Search framework with all 15 employees
2. `CAPTCHA_BYPASS_OPTIONS.md` - Detailed bypass options
3. `MANUAL_CAPTCHA_INSTRUCTIONS.md` - Step-by-step manual process
4. `MARYLAND_SEARCH_STRATEGY.md` - This file (complete strategy)

## Next Action

**IMMEDIATE:** Begin Phase 1 - Manual CAPTCHA for Edward Hyland
1. Navigate to Maryland DLLR search page
2. Fill "Hyland" in Last Name field
3. **WAIT FOR USER** to complete CAPTCHA
4. Continue with search execution
