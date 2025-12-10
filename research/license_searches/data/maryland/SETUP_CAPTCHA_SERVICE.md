# Setting Up CAPTCHA Solving Service for Maryland Searches

**Date:** December 7, 2025
**Purpose:** Automate remaining 12 employee searches after high-priority manual searches

## Quick Start

### Step 1: Choose a Service

**Recommended: Anti-Captcha** (cheapest at $0.001 per CAPTCHA)

1. **2Captcha** - https://2captcha.com
   - Cost: $2.99 per 1000 CAPTCHAs (~$0.003 per search)
   - Success Rate: ~95%
   - Speed: 10-30 seconds per CAPTCHA

2. **Anti-Captcha** - https://anti-captcha.com ⭐ RECOMMENDED
   - Cost: $1.00 per 1000 CAPTCHAs (~$0.001 per search)
   - Success Rate: ~98%
   - Speed: 10-20 seconds per CAPTCHA

3. **CapSolver** - https://capsolver.com
   - Cost: $1.50 per 1000 CAPTCHAs (~$0.0015 per search)
   - Success Rate: ~96%
   - Speed: 15-25 seconds per CAPTCHA

### Step 2: Sign Up and Get API Key

1. Create account on chosen service
2. Add funds (minimum usually $2-5)
3. Copy your API key from dashboard

### Step 3: Install Library

**For Node.js/Playwright:**
```bash
npm install playwright-recaptcha
```

**For Python/Playwright:**
```bash
pip install playwright-recaptcha
```

### Step 4: Implement in Script

**JavaScript Example:**
```javascript
const { solveRecaptcha } = require('playwright-recaptcha');

// Navigate to Maryland DLLR
await page.goto('https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name');

// Fill form
await page.fill('input[type="text"]', 'Fisher');

// Solve CAPTCHA automatically
await solveRecaptcha(page, {
  apiKey: 'YOUR_API_KEY',
  provider: 'anticaptcha' // or '2captcha', 'capsolver'
});

// Click search (button should now be enabled)
await page.click('button[type="submit"]');

// Extract results
const results = await page.evaluate(() => {
  // Extract license information
});
```

**Python Example:**
```python
from playwright_recaptcha import solve_recaptcha

# Navigate to Maryland DLLR
await page.goto('https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name')

# Fill form
await page.fill('input[type="text"]', 'Fisher')

# Solve CAPTCHA automatically
await solve_recaptcha(page, api_key='YOUR_API_KEY', provider='anticaptcha')

# Click search
await page.click('button[type="submit"]')
```

## Cost Estimate

For 12 medium-priority employees:
- **2Captcha:** $0.036 (3.6 cents)
- **Anti-Captcha:** $0.012 (1.2 cents) ⭐
- **CapSolver:** $0.018 (1.8 cents)

**Recommendation:** Use Anti-Captcha for lowest cost.

## Testing

Before running all 12 searches, test with one employee:

1. Use "Cindy Fisher" as test case
2. Verify CAPTCHA is solved correctly
3. Verify search executes and results are extracted
4. If successful, proceed with remaining 11 employees

## Employees to Search (Medium Priority)

1. Cindy Fisher
2. Luke Davis
3. Pat Cassada
4. Sean Curtin
5. Amy Groff
6. Robert Grealy
7. Djene Moyer
8. Henry Ramos
9. Kristina Thoummarath
10. Christina Chang
11. Todd Bowen
12. Jeffrey Williams

## Alternative: Continue Manual CAPTCHA

If you prefer not to use a service:
- Continue with manual CAPTCHA for remaining employees
- Estimated time: 30-40 minutes for 12 employees
- No cost, but more time-consuming

## Next Steps

1. ✅ Choose service (recommend Anti-Captcha)
2. ✅ Sign up and get API key
3. ✅ Install library
4. ⏳ Test with one employee
5. ⏳ Run automated searches for remaining 11 employees
6. ⏳ Document all results
