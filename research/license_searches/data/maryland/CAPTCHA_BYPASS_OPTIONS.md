# Maryland DLLR CAPTCHA Bypass Options

**Date:** December 7, 2025
**URL:** https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name

## CAPTCHA Analysis

### Type: reCAPTCHA v2
- **Implementation:** Google reCAPTCHA v2 ("I'm not a robot" checkbox)
- **Location:** Embedded in iframe before search button
- **Site Key:** `6LeUU6ApAAAAANxcBOW8c_zqA8mPt2fjzW1KY7aw`
- **Behavior:** Search button disabled until CAPTCHA completed

## Bypass Options

### Option 1: Manual CAPTCHA Completion with Automation
**Approach:** Wait for user to manually complete CAPTCHA, then continue automation

**Implementation:**
```javascript
// Wait for CAPTCHA to be completed (check if search button becomes enabled)
await page.waitForFunction(
  () => {
    const button = document.querySelector('button[type="submit"], input[type="submit"]');
    return button && !button.disabled;
  },
  { timeout: 300000 } // 5 minute timeout for manual completion
);
```

**Pros:**
- Legitimate and ethical
- No terms of service violation
- Reliable

**Cons:**
- Requires manual intervention for each search
- Time-consuming for 15 employees

### Option 2: CAPTCHA Solving Service Integration
**Approach:** Use a CAPTCHA solving service (2Captcha, Anti-Captcha, CapSolver)

**Services Available:**
1. **2Captcha** - https://2captcha.com
2. **Anti-Captcha** - https://anti-captcha.com
3. **CapSolver** - https://capsolver.com
4. **Playwright-reCAPTCHA** library - https://github.com/Xewdy444/Playwright-reCAPTCHA

**Implementation Example:**
```javascript
// Using playwright-recaptcha library
const { solveRecaptcha } = require('playwright-recaptcha');

await solveRecaptcha(page);
```

**Pros:**
- Fully automated
- Can handle multiple searches
- Relatively fast

**Cons:**
- Costs money (typically $1-3 per 1000 CAPTCHAs)
- May violate terms of service
- Requires API key setup

### Option 3: Alternative Data Sources
**Approach:** Contact Maryland Real Estate Commission directly for data

**Contact Information:**
- **Address:** 100 S. Charles Street, Tower 1, Baltimore, MD 21201
- **Phone:** 410-230-6200
- **Email:** dlmrec-labor@maryland.gov

**Request:**
- Bulk license data export
- API access for research purposes
- CSV/Excel file of all active licenses

**Pros:**
- Most legitimate approach
- No CAPTCHA issues
- May get more complete data

**Cons:**
- Requires waiting for response
- May not be available
- May require formal request process

### Option 4: Session Persistence
**Approach:** Complete CAPTCHA once, maintain session cookies

**Implementation:**
```javascript
// Save browser context after manual CAPTCHA
const context = await browser.newContext();
await context.addCookies(/* cookies from manual session */);
```

**Pros:**
- Can reuse session
- May work for multiple searches

**Cons:**
- CAPTCHA may expire
- Session may timeout
- Not guaranteed to work

### Option 5: Direct Form Submission (Bypass)
**Approach:** Attempt to submit form directly without CAPTCHA

**Note:** This is unlikely to work as the server validates the reCAPTCHA token.

## Recommended Approach

### Hybrid Strategy:
1. **Immediate:** Use Option 1 (Manual CAPTCHA) for critical searches (Edward Hyland, Robert Kettler, Caitlin Skidmore)
2. **Short-term:** Set up Option 2 (CAPTCHA service) for remaining 12 employees
3. **Long-term:** Submit Option 3 (Direct request) to Maryland Real Estate Commission

## Implementation Priority

1. **High Priority (Manual):**
   - Edward Hyland
   - Robert Kettler
   - Caitlin Skidmore

2. **Medium Priority (Service or Manual):**
   - Remaining 12 employees

3. **Low Priority (Can wait for commission response):**
   - All employees if commission provides bulk data

## Legal and Ethical Considerations

- **Terms of Service:** Review Maryland DLLR terms of service before using automated tools
- **Rate Limiting:** Implement delays between searches to avoid overwhelming server
- **Purpose:** Ensure searches are for legitimate research/investigation purposes
- **Data Usage:** Use data responsibly and in accordance with applicable laws

## Next Steps

1. Test manual CAPTCHA completion with automation continuation
2. Evaluate CAPTCHA solving service costs and setup
3. Draft email to Maryland Real Estate Commission requesting bulk data
4. Document which approach works best for this use case
